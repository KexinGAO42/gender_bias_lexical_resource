import csv

# Path to the input CSV file
input_csv_path = '1a.csv'

# Path to the output CSV file
output_csv_path = '1a_modified.csv'

# Open the input CSV file for reading and the output CSV file for writing
with open(input_csv_path, 'r', newline='') as input_file, open(output_csv_path, 'w', newline='') as output_file:
    # Create a CSV reader and writer objects
    reader = csv.reader(input_file)
    writer = csv.writer(output_file)

    # Iterate through each row in the input CSV file
    for row in reader:
        print(row)
        # Modify each cell in the row according to the specified rules
        modified_row = [row[0]]

        if not row[1]:
            row[1] = 'N'
        modified_row.append(row[1])

        modified_row.append(row[2])

        # Add "\\" at the end of each line
        modified_row[-1] += '\\\\'

        new_row = "&".join(modified_row)

        # Write the modified row to the output CSV file
        writer.writerow([new_row])

print("Modifications complete. Output CSV file saved successfully.")