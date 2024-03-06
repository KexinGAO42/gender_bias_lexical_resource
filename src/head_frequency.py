import pandas as pd

# Load the CSV file into a pandas DataFrame
df = pd.read_csv("gender_labeled_r4.csv")

# Create an empty dictionary to store head frequencies
head_frequency_dict = {}

# Iterate through rows in the DataFrame
for index, row in df.iterrows():
    head = row["Head"]

    # Check if the head is not empty
    if pd.notna(head):
        # Increment the frequency count for the head in the dictionary
        head_frequency_dict[head] = head_frequency_dict.get(head, 0) + 1

# Sort the dictionary by values in descending order
sorted_head_frequency = dict(sorted(head_frequency_dict.items(), key=lambda item: item[1], reverse=True))

# Print or use the sorted dictionary as needed
print(sorted_head_frequency)
print(len(sorted_head_frequency))