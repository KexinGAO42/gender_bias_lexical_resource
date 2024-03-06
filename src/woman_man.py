import pandas as pd
from tqdm import tqdm


# Load CSV file into DataFrame
df = pd.read_csv("gender_synset_based_new_4.csv")


def end_with_woman(word):
    lowercase_word = word.lower()
    return lowercase_word.endswith("woman")


def end_with_man(word):
    lowercase_word = word.lower()
    return lowercase_word.endswith("man") and not lowercase_word.endswith("woman")


def replace_woman_with_man(word):
    return word.replace("woman", "man")


def replace_man_with_woman(word):
    return word.replace("man", "woman")


def replace_woman_with_person(word):
    return word.replace("woman", "person")


def replace_woman_with_people(word):
    return word.replace("woman", "people")


def replace_man_with_person(word):
    return word.replace("man", "person")


def replace_man_with_people(word):
    return word.replace("man", "people")


result_df = pd.DataFrame(columns=["root", "m_lemma", "m_gender", "m_definition",
                                  "f_lemma", "f_gender", "f_definition",
                                  "n_lemma", "n_gender", "n_definition"])


# woman_based extraction
for index, row in df.iterrows():

    lemma = str(row["Lemma"])
    gender = row["Gender"]
    definition = row["Definition"]

    if end_with_woman(lemma):

        # Store root and woman_based info
        root = lemma.replace("woman", "")
        woman_version = lemma
        woman_def = definition
        woman_gender = gender

        m_version, man_gender, man_def, n_version, neu_gender, neu_def = "", "", "", "", "", ""

        # Check man version exists or not
        man_version = replace_woman_with_man(lemma)
        man_row = df[df["Lemma"] == man_version]
        if not man_row.empty:
            man_gender = man_row.iloc[0]["Gender"]
            m_version = man_version
            man_def = man_row.iloc[0]["Definition"]

        neu_version = replace_woman_with_person(lemma)
        neu_row = df[df["Lemma"] == neu_version]
        if not neu_row.empty:
            n_version = neu_version
            neu_gender = neu_row.iloc[0]["Gender"]
            neu_def = neu_row.iloc[0]["Definition"]
        else:
            neu_version = replace_woman_with_people(lemma)
            neu_row = df[df["Lemma"] == neu_version]
            if not neu_row.empty:
                n_version = neu_version
                neu_gender = neu_row.iloc[0]["Gender"]
                neu_def = neu_row.iloc[0]["Definition"]

        result_df = result_df.append({
            "root": root,
            "f_lemma": woman_version,
            "f_gender": woman_gender,
            "f_definition": woman_def,
            "m_lemma": m_version,
            "m_gender": man_gender,
            "m_definition": man_def,
            "n_lemma": n_version,
            "n_gender": neu_gender,
            "n_definition": neu_def
        }, ignore_index=True)


# man_based extraction
for index, row in df.iterrows():

    lemma = str(row["Lemma"])
    gender = row["Gender"]
    definition = row["Definition"]

    if end_with_man(lemma) and gender != "PPN":

        # check whether the root is already stored
        root = lemma.replace("man", "")
        root_row = result_df[result_df["root"] == root]

        if root_row.empty:
            man_version = lemma
            man_def = definition
            man_gender = gender

            f_version, woman_gender, woman_def, n_version, neu_gender, neu_def = "", "", "", "", "", ""

            # Check woman version exists or not
            woman_version = replace_man_with_woman(lemma)
            woman_row = df[df["Lemma"] == woman_version]
            if not woman_row.empty:
                woman_gender = woman_row.iloc[0]["Gender"]
                f_version = woman_version
                woman_def = woman_row.iloc[0]["Definition"]

            # Check neutral version exists or not
            neu_version = replace_man_with_person(lemma)
            neu_row = df[df["Lemma"] == neu_version]
            if not neu_row.empty:
                n_version = neu_version
                neu_gender = neu_row.iloc[0]["Gender"]
                neu_def = neu_row.iloc[0]["Definition"]
            else:
                neu_version = replace_man_with_people(lemma)
                neu_row = df[df["Lemma"] == neu_version]
                if not neu_row.empty:
                    n_version = neu_version
                    neu_gender = neu_row.iloc[0]["Gender"]
                    neu_def = neu_row.iloc[0]["Definition"]

            result_df = result_df.append({
                "root": root,
                "f_lemma": f_version,
                "f_gender": woman_gender,
                "f_definition": woman_def,
                "m_lemma": man_version,
                "m_gender": man_gender,
                "m_definition": man_def,
                "n_lemma": n_version,
                "n_gender": neu_gender,
                "n_definition": neu_def
            }, ignore_index=True)



result_df.to_csv("suffix_data_1.csv", index=False)


"""
Code:
1. woman_based
    a. get words ending with "woman"
    b. check man version
    c. check neutral version
2. man_based
    a. get words ending with "man" but not "woman"
    b. check woman version
    c. check neutral version
3. neutral_based (no -man/-woman version)

"""


"""
Output df structure

root    man_version     man_version_gender    man_version_def               woman_version    woman_version_gender    woman_version_def      neutral_version
law     lawman          N                     an officer of the law         NA               NA                      NA                     NA
news    newsman         N                     a person who investigates..   newswoman        F                       a female newsperson    newsperson
"""

"""
Stats


"""