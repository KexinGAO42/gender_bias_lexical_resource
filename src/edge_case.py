import pandas as pd
from pycorenlp import StanfordCoreNLP
from tqdm import tqdm


# Load CSV file into DataFrame
df = pd.read_csv("gender_compound_based.csv")

# Set up CoreNLP client
nlp = StanfordCoreNLP('http://localhost:9000')


# Function to label gender based on head and modifier
def label_gender(definition):

    result = {"head": "", "amod": "", "gender": ""}

    # Parse definition with CoreNLP API
    parse_result = nlp.annotate(definition, properties={
        'annotators': 'depparse',
        'outputFormat': 'json'
    })

    # Check whether the root is VBD or VBN and get the real root
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

            dependencies = new_parse_result['sentences'][0]['basicDependencies']

            root = new_parse_result['sentences'][0]['basicDependencies'][0]['dependentGloss']
            # Check head for gender keywords
            if root.lower() in female_keywords:
                result["head"] = root
                result["gender"] = "F"
            if root.lower() in male_keywords:
                result["head"] = root
                result["gender"] = "M"

            # Check modifier / compound of the head for gender keywords; overwrite the gender
            for word in dependencies:
                if word['dep'] == 'amod' or word['dep'] == 'compound':
                    if word['governorGloss'] == root:
                        if word['dependentGloss'].lower() in female_keywords:
                            result["amod"] = word['dependentGloss']
                            result["gender"] = "F"
                        elif word['dependentGloss'].lower() in male_keywords:
                            result["amod"] = word['dependentGloss']
                            result["gender"] = "M"

            # If still no gender and head in neutral keywords, label as neutral
            if not result["gender"]:
                if root.lower() in neutral_keywords:
                    result["gender"] = "N"
                    result["head"] = root

    return result


# # Keywords for gender labeling
female_keywords = ["woman", "female", "lady", "girl", "mother", "daughter",
                   "grandmother", "wife", "maid", "maiden", "aunt", "niece",
                   "sister", "nanny", "princess", "duchess", "widow", "girlfriend",
                   "fiancee", "matron", "madam", "diva", "goddess"]
male_keywords = ["man", "male", "boy", "son", "father", "husband",
                 "grandfather", "uncle", "nephew", "brother", "prince", "duke", "widower",
                 "gentleman", "sir", "mister", "fiance", "emperor"]
neutral_keywords = ["one", "person", "someone", "member"]

new = []
# Iterate through rows and label gender
for index, row in tqdm(df.iterrows(), total=len(df), desc="Processing"):
    gender = row["Gender"]
    definition = row["Definition"]
    # process labeling for unlabeled lemma
    if pd.isna(gender):
        result = label_gender(definition)
        df.at[index, "Head"] = result["head"]
        df.at[index, "Gender"] = result["gender"]
        df.at[index, "Amod/Comp"] = result["amod"]
        new.append((result["gender"], definition))

# Save result to a new CSV file
df.to_csv("gender_edge_case.csv", index=False)

print("Gender labeling completed. Results saved to gender_labeled_r1.csv.")
print(new)


