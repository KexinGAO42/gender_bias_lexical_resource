import pandas as pd
from pycorenlp import StanfordCoreNLP
from tqdm import tqdm
from nltk.corpus import wordnet


# Set up CoreNLP client
nlp = StanfordCoreNLP('http://localhost:9001')
# Load the CSV file into a pandas DataFrame
df = pd.read_csv("gender_edge_case_2.csv")


# Create a dictionary to store the gender labels for each synset
synset_gender_dict = {}
for index, row in df.iterrows():
    synset = row["Sense"]
    gender = row["Gender"]

    # Check if the gender is undecided ("")
    if pd.notna(gender):
        # Check if the synset is already in the dictionary
        synset_gender_dict[synset] = gender


# Iterate through rows in the DataFrame
lemma_synsets_dict = {}
for index, row in df.iterrows():
    synset = row["Sense"]
    lemma = row["Lemma"]

    if lemma not in lemma_synsets_dict:
        lemma_synsets_dict[lemma] = []
    lemma_synsets_dict[lemma].append(synset)

new_added = []
# Iterate through rows in the DataFrame
for index, row in tqdm(df.iterrows(), total=len(df), desc="Processing"):
    sense = row["Sense"]
    gender = row["Gender"]
    definition = row["Definition"]
    lemma = row["Lemma"]

    # Check if the gender is undecided ("")
    if pd.isna(gender):
        # Check if the synset is already in the dictionary
        parse_result = nlp.annotate(definition, properties={
            'annotators': 'depparse',
            'outputFormat': 'json'
        })

        # Get head of the sentence
        root = parse_result['sentences'][0]['basicDependencies'][0]['dependentGloss']
        # Check if the root is correct (not VBD/VBN)
        root_index = parse_result['sentences'][0]['basicDependencies'][0]['dependent']
        root_pos = parse_result['sentences'][0]['tokens'][root_index - 1]['pos']
        if root_pos == 'VBD' or root_pos == 'VBN':
            real_root = []
            for i in range(root_index - 1):
                real_root.append(parse_result['sentences'][0]['tokens'][i]['word'])
            real_root = " ".join(real_root)

            if real_root:
                new_parse_result = nlp.annotate(real_root, properties={
                    'annotators': 'depparse',
                    'outputFormat': 'json'
                })

                root = new_parse_result['sentences'][0]['basicDependencies'][0]['dependentGloss']

        root = root.lower()
        # Get the synsets of the roots
        if root in lemma_synsets_dict:
            max_dist, res = 0, None
            root_synsets = lemma_synsets_dict[root]
            for root_synset in root_synsets:
                distance = wordnet.synset(sense).path_similarity(wordnet.synset(root_synset))
                if distance > max_dist:
                    max_dist = distance
                    res = root_synset
            if res in synset_gender_dict:
                df.at[index, "Gender"] = synset_gender_dict[res]
                new_added.append((lemma, definition, res, synset_gender_dict[res]))


# Save the updated DataFrame to a new CSV file
df.to_csv("gender_synset_based_new_4_new.csv", index=False)
print(new_added)
print(len(new_added))
