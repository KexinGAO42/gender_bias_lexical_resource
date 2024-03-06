import pandas as pd
from pycorenlp import StanfordCoreNLP
from tqdm import tqdm


# Load CSV file into DataFrame
df = pd.read_csv("gender_labeled_r1.csv")

# Set up CoreNLP client
nlp = StanfordCoreNLP('http://localhost:9000')

sentence = "a bishop having jurisdiction over a diocese"
parse_result = nlp.annotate(sentence, properties={
    'annotators': 'depparse',
    'outputFormat': 'json'
})
print(parse_result)

root = parse_result['sentences'][0]['basicDependencies'][0]['dependentGloss']
root_index = parse_result['sentences'][0]['basicDependencies'][0]['dependent']
root_pos = parse_result['sentences'][0]['tokens'][root_index - 1]['pos']
if root_pos == 'VBD' or root_pos == 'VBN':
    real_root = []
    for i in range(root_index - 1):
        real_root.append(parse_result['sentences'][0]['tokens'][i]['word'])
real_root = " ".join(real_root)

new_parse_result = parse_result = nlp.annotate(real_root, properties={
    'annotators': 'depparse',
    'outputFormat': 'json',
    'depparse.model': 'edu/stanford/nlp/models/parser/nndep/english_UD.gz'
})

print(new_parse_result)


# # Create a new DataFrame for results
# result_df = pd.DataFrame(columns=["Lemma", "Sense", "SuperSense", "POS_Tag", "Definition", "Head", "HeadAmod", "Gender"])
#
# # Iterate through rows and label gender
# for index, row in tqdm(df.iterrows(), total=len(df), desc="Processing"):
#     gender = row["Gender"]
#     if pd.isna(gender):
#         result = label_gender(row["Definition"])
#         result_df = result_df.append({
#             "Lemma": row["Lemma"],
#             "Sense": row["Sense"],
#             "SuperSense": row["SuperSense"],
#             "POS_Tag": row["POS_Tag"],
#             "Definition": row["Definition"],
#             "Examples": row["Examples"],
#             "Head": result["head"],
#             "Gender": result["gender"]
#         }, ignore_index=True)
#
# # Save result to a new CSV file
# result_df.to_csv("gender_labeled_r1_n.csv", index=False)
#
# print("Gender labeling completed. Results saved to gender_labeled_r1.csv.")


