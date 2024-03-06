import csv
import re
import pandas as pd
from pycorenlp import StanfordCoreNLP
from tqdm import tqdm


# Set up CoreNLP client
nlp = StanfordCoreNLP('http://localhost:9000')

# Load the CSV file into a pandas DataFrame
file_path = 'gender_labeled_r3.csv'  # Update with your actual file path
df = pd.read_csv(file_path)

# Create a dictionary for gender-marked lemmas
gender_marked = {}

for index, row in tqdm(df.iterrows(), total=len(df), desc="Processing"):
    lemma = row['Lemma']
    gender = row['Gender']
    if pd.notna(gender) and lemma not in gender_marked:
        gender_marked[lemma] = gender
    elif pd.notna(gender) and lemma in gender_marked and gender_marked[lemma] != gender:
        del gender_marked[lemma]


def label_gender(row, definition):

    # Parse definition with CoreNLP API
    parse_result = nlp.annotate(definition, properties={
        'annotators': 'depparse',
        'outputFormat': 'json'
    })

    # Get head of the sentence
    root = parse_result['sentences'][0]['basicDependencies'][0]['dependentGloss']

    # Check head for gender keywords
    if root.lower() in gender_marked:
        row['Gender'] = gender_marked[root.lower()]
        row['Head'] = root.lower()
        newly_added.append((row['Lemma'], definition))
    else:
        # Check modifier of the head for gender keywords
        for word in parse_result['sentences'][0]['basicDependencies']:
            if word['dep'] == 'amod' and word['governorGloss'] == root:
                if word['dependentGloss'].lower() in gender_marked:
                    row["HeadAmod"] = word['dependentGloss']
                    row["Gender"] = gender_marked[word['dependentGloss'].lower()]


newly_added = []
for index, row in tqdm(df.iterrows(), total=len(df), desc="Processing"):
    definition = row['Definition']
    gender = row['Gender']
    if not pd.notna(gender):
        label_gender(row, definition)

# Save result to a new CSV file
df.to_csv("gender_labeled_r4.csv", index=False)

print(newly_added)
print("Gender labeling completed. Results saved to gender_labeled_r2_backup.csv.")
