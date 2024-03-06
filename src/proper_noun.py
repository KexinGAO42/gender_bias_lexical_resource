import re
import pandas as pd


def find_year_in_string(input_string):
    # Define a regular expression pattern to match four consecutive digits
    pattern_1 = r'\b\d{4}\b'
    pattern_2 = r'\b\d{3}\b'

    # Use re.findall to find all occurrences of the pattern in the input string
    matches = re.findall(pattern_1, input_string) or re.findall(pattern_2, input_string)

    # If matches are found, return True; otherwise, return False
    return bool(matches)


def find_pattern_in_string(input_string):
    patterns = ['(Greek mythology)', '(classical mythology)', '(Norse mythology)',
                '(New Testament)', '(Old Testament)', '(Roman mythology)', '(Arthurian legend)',
                ' BC', ' AD', '(Hindu mythology)', '(Irish folklore)', ]
    for pattern in patterns:
        if pattern in input_string:
            return True


# Load the CSV file into a pandas DataFrame
df = pd.read_csv("gender_synset_based_new_3.csv")

for index, row in df.iterrows():
    definition = row["Definition"]
    year = find_year_in_string(definition)
    myth = find_pattern_in_string(definition)
    if myth or year:
        df.at[index, "Gender"] = "PPN"


df.to_csv("gender_PPN_removed_new_1.csv", index=False)
