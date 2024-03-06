import csv
from nltk.corpus import wordnet
from tqdm import tqdm


out = wordnet.get_version()
print(out)

def extract_wordnet_info():
    data = []

    all_lemmas = wordnet.all_lemma_names()

    for lemma_name in tqdm(all_lemmas, desc="Processing Lemmas", unit="lemma"):
        synsets = wordnet.synsets(lemma_name)

        if synsets:
            for synset in synsets:
                sense = synset.name()
                supersense = synset.lexname()
                pos_tag = synset.pos()
                definition = synset.definition()
                examples = synset.examples()

                data.append({
                    'Lemma': lemma_name,
                    'Sense': sense,
                    'SuperSense': supersense,
                    'POS_Tag': pos_tag,
                    'Definition': definition,
                    'Examples': examples
                })

    return data


# def save_to_csv(data, file_path='wordnet_lemma_data.csv'):
#     fields = ['Lemma', 'Sense', 'SuperSense', 'POS_Tag', 'Definition', 'Examples']
#
#     with open(file_path, 'w', newline='') as csvfile:
#         writer = csv.DictWriter(csvfile, fieldnames=fields)
#         writer.writeheader()
#         writer.writerows(data)


# if __name__ == "__main__":
#     wordnet_data = extract_wordnet_info()
#     # save_to_csv(wordnet_data)
#     print(len(wordnet_data))
#     print("Data saved to 'wordnet_lemma_data.csv'")


"""
todo1:
identify a list of person nouns and label each one automatically based on definition
Parse the definition or use better heuristics
Do it several rounds
# First round: root is gendered -> root is not gendered but amod of root is gendered
# Second round: remove 

todo2:
-man vs. -woman vs -person
-or vs -tress (find a list of male suffix and female suffix)
calc P(word w/ woman suffix  | word w/ -man suffix)
P(manW is gender neutral | both manW and womanW exist)
Dump out the list of manW
manW womanW personW

todo3:
check the definition to look for the list of words where the words are general-neutral but the definition uses something like “himself”
You have to first use heuristic to filter out proper nouns

todo4:
check examples
For definition and example: gender has a few cases: male only, female only, both, and neural
collect the prob
P(genderOfDef | genderOfEntry)
P(genderOfEx | genderOfEntry)

todo6:
from the lists you got, check our edu corpora
"""
