import re
import pandas as pd

def native(input_string):
    input_string = input_string.split(" ")
    if input_string[0] == "a" and input_string[1] == "native":
        return True
    else:
        return False


# Load the CSV file into a pandas DataFrame
df = pd.read_csv("gender_PPN_removed_new_1.csv")

for index, row in df.iterrows():
    definition = row["Definition"]
    if native(definition):
        df.at[index, "Gender"] = "N"


df.to_csv("gender_edge_case_2.csv", index=False)
