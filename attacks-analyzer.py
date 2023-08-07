import zipfile
import sys
import pandas as pd
import os

# Define color codes for text formatting
RESET = '\033[0m'
BOLD = '\033[01m'

# Function to extract files from a zip archive
def extract_file(zip_path, file_to_extract, output_dir):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extract(file_to_extract, path=output_dir)

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Example usage
zip_path = sys.argv[1]
file1_to_extract = 'all-strikes-attack.csv'
file2_to_extract = 'all-encrypted-attacks-attack.csv'
output_dir = './csvs/pytemp/'

# Extract the specified files from the zip archive
extract_file(zip_path, file1_to_extract, output_dir)
extract_file(zip_path, file2_to_extract, output_dir)

# Define file paths for the extracted CSV files
csv_path = './csvs/pytemp/all-strikes-attack.csv'
csv2_path = './csvs/pytemp/all-encrypted-attacks-attack.csv'

# Read the CSV files into DataFrames, parsing date columns
df1 = pd.read_csv(csv_path, parse_dates=['Timestamp'])
df2 = pd.read_csv(csv2_path, parse_dates=['Timestamp'])

# Convert Timestamp to datetime type
df1['Timestamp'] = pd.to_datetime(df1['Timestamp'])
df2['Timestamp'] = pd.to_datetime(df2['Timestamp'])

#--------------------------
# Extract unique attack names from the DataFrames
uniq_attacks = df1['Action name'].unique()
uniq_encrypted_attacks = df2['Action name'].unique()

# Count the number of unique attacks
uniq_attacks_count = len(uniq_attacks)
uniq_encrypted_attacks_count = len(uniq_encrypted_attacks)

# Select the last entries in the DataFrames based on unique attacks count
last_attacks_entries = df1.tail(uniq_attacks_count)
last_encrypted_attacks_entries = df2.tail(uniq_encrypted_attacks_count)

# Concatenate the last entries from both DataFrames
df3 = pd.concat([last_attacks_entries, last_encrypted_attacks_entries])

# Calculate block rate using a lambda function and add it as a new column
df3 = df3.assign(Block_Rate = (lambda x: (x['Client Blocked']/x['Client Started'] * 100)))

# Select specific columns for the new DataFrame
df3 = df3[['Timestamp', 'Action name', 'Block_Rate']].copy()

# Filter DataFrames based on block rate values
df4 = df3[df3['Block_Rate']==100]
df5 = df3[df3['Block_Rate']==0]
df6 = df3[df3['Block_Rate']==range(1,99)]

# Calculate counts and block rate statistics
Total_Initiated_Attacks_Count = len(df3)
Fully_Blocked_Attacks_Count = len(df4)
Fully_Allowed_Attacks_Count = len(df5)
Partially_Blocked_Attacks_Count = len(df6)

Block_Rate = Fully_Blocked_Attacks_Count/Total_Initiated_Attacks_Count * 100

# Print the calculated statistics
print(f"Total Initiated Attacks: {Total_Initiated_Attacks_Count}\n")
print(f"Fully Blocked Attacks: {Fully_Blocked_Attacks_Count}")
print(f"Fully Allowed Attacks: {Fully_Allowed_Attacks_Count}")
print(f"Partially Blocked Attacks: {Partially_Blocked_Attacks_Count}")
print(f"\nBlock Rate: {BOLD}{Block_Rate} %{RESET}")

# Save fully blocked attacks to a CSV file
df4.to_csv(f"./csvs/stats/{zip_path}_all_unique_attacks.csv")
