import pandas as pd
from pycorenlp import StanfordCoreNLP
from tqdm import tqdm


# Load CSV file into DataFrame
df = pd.read_csv("wordnet_lemma_data.csv")

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

    # Get head of the sentence
    dependencies = parse_result['sentences'][0]['basicDependencies']
    root = dependencies[0]['dependentGloss']
    result["head"] = root


    # Check head for gender keywords
    if root.lower() in female_keywords:
        result["gender"] = "F"
    if root.lower() in male_keywords:
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


# Create a new DataFrame for results
result_df = pd.DataFrame(columns=["Lemma", "Sense", "SuperSense", "POS_Tag", "Definition", "Examples", "Head", "Amod/Comp", "Gender"])

# Iterate through rows and label gender
for index, row in tqdm(df.iterrows(), total=len(df), desc="Processing"):
    if row["SuperSense"] == "noun.person":
        if row["Lemma"] in female_keywords:
            result = {"head": "", "amod": "", "gender": "F"}
        elif row["Lemma"] in male_keywords:
            result = {"head": "", "amod": "", "gender": "M"}
        else:
            result = label_gender(row["Definition"])
        result_df = result_df.append({
            "Lemma": row["Lemma"],
            "Sense": row["Sense"],
            "SuperSense": row["SuperSense"],
            "POS_Tag": row["POS_Tag"],
            "Definition": row["Definition"],
            "Examples": row["Examples"],
            "Head": result["head"],
            "Amod/Comp": result["amod"],
            "Gender": result["gender"]
        }, ignore_index=True)

# Save result to a new CSV file
result_df.to_csv("gender_keyword_based_new.csv", index=False)

print("Gender labeling completed. Results saved to gender_labeled_r1.csv.")


