import pandas as pd
from tqdm import tqdm


# Load CSV file into DataFrame
df = pd.read_csv("gender_keyword_based_new.csv")

new = []
# Iterate through rows and label gender
for index, row in tqdm(df.iterrows(), total=len(df), desc="Processing"):
    lemma = str(row["Lemma"])
    gender = row["Gender"]
    definition = row["Definition"]
    if "woman" in lemma.lower():
        if gender == "N" or pd.isna(gender):
            df.at[index, "Gender"] = "F"
            new.append((lemma, definition))

# Save result to a new CSV file
df.to_csv("gender_compound_based.csv", index=False)

print("Gender labeling completed. Results saved to gender_labeled_r1.csv.")
print(new)
print(len(new))