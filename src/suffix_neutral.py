import pandas as pd
from tqdm import tqdm


# Load CSV file into DataFrame
df = pd.read_csv("gender_synset_based_new_4.csv")


def end_with_people_or_person(word):
    lowercase_word = word.lower()
    return lowercase_word.endswith("people") or lowercase_word.endswith("person")


result_df = pd.DataFrame(columns=["root", "m_lemma", "m_gender", "m_definition",
                                  "f_lemma", "f_gender", "f_definition",
                                  "n_lemma", "n_gender", "n_definition"])


# woman_based extraction
for index, row in df.iterrows():

    lemma = str(row["Lemma"])
    gender = row["Gender"]
    definition = row["Definition"]

    if end_with_people_or_person(lemma):

        # Store root and woman_based info
        if "people" in lemma:
            root = lemma.replace("people", "")
        if "person" in lemma:
            root = lemma.replace("person", "")
        woman_version = root + "woman"
        man_version = root + "man"

        man_row = df[df["Lemma"] == man_version]
        woman_row = df[df["Lemma"] == woman_version]

        print(man_version, woman_version)
        print(man_row.empty, woman_row.empty)

        if man_row.empty:
            if woman_row.empty:
                print(lemma)
                m_version, m_gender, m_def, f_version, f_gender, f_def = "", "", "", "", "", ""

                result_df = result_df.append({
                    "root": root,
                    "f_lemma": f_version,
                    "f_gender": f_gender,
                    "f_definition": f_def,
                    "m_lemma": m_version,
                    "m_gender": m_gender,
                    "m_definition": m_def,
                    "n_lemma": lemma,
                    "n_gender": gender,
                    "n_definition": definition
                }, ignore_index=True)

result_df.to_csv("suffix_data_n_1.csv", index=False)