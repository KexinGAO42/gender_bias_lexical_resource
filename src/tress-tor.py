import pandas as pd
from tqdm import tqdm


# Load CSV file into DataFrame
df = pd.read_csv("gender_synset_based_new_4.csv")

lemma_dict = {}


def contains_woman(word):
    return "tress" in word.lower()

def replace_woman_with_man(word):
    return word.replace("tress", "tor")

def replace_woman_with_man_2(word):
    return word.replace("tress", "ter")

count = 0
for index, row in df.iterrows():
    lemma = str(row["Lemma"])
    gender = row["Gender"]
    definition = row["Definition"]
    if contains_woman(lemma):
        man_version = replace_woman_with_man(lemma)
        man_row = df[df["Lemma"] == man_version]
        if not man_row.empty:
            man_gender = man_row.iloc[0]["Gender"]
            man_def = man_row.iloc[0]["Definition"]
            print("{}, {}, {}".format(man_version, man_gender, man_def))
        else:
            man_version = replace_woman_with_man_2(lemma)
            man_row = df[df["Lemma"] == man_version]
            if not man_row.empty:
                man_gender = man_row.iloc[0]["Gender"]
                man_def = man_row.iloc[0]["Definition"]
                print("{}, {}, {}".format(man_version, man_gender, man_def))
            else:
                print('NA')

        # neutral_version = replace_woman_with_person(lemma)
        # neu_row = df[df["Lemma"] == neutral_version]
        # if not neu_row.empty:
        #     neu_gender = neu_row.iloc[0]["Gender"]
        #     neu_def = neu_row.iloc[0]["Definition"]
        #     print("{}, {}, {}".format(neutral_version, neu_gender, neu_def))
        # else:
        #     print('NA')
        print("{}, {}, {}".format(lemma, gender, definition))

print(count)
