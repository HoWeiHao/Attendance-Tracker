import pandas as pd
import os

# Function to read either Excel or CSV files
def read_file(file_path):
    if file_path.endswith('.csv'):
        return pd.read_csv(file_path, header=5), pd.read_csv(file_path, header=None).iloc[2, 0] # For CSV files
    else:
        raise ValueError("Unsupported file format")

# Function to process each input file and update the consolidated DataFrame
def process_file(file_path, consolidated_df):
    # Read the file (CSV or Excel)
    df, event_name = read_file(file_path)
    
    # Concatenate First Name and Last Name to create a full name
    df['Full Name'] = str(df['First Name']) + ' ' + str(df['Last Name'])

    # Select relevant columns
    df = df[['Full Name', 'Campus Email', 'Card ID Number']].copy()
    
    # Add a column for the event attendance, marking everyone as present (1)
    df[event_name] = 1

    # Ensure the columns used for merging have consistent data types
    df['Full Name'] = df['Full Name'].astype(str)
    df['Campus Email'] = df['Campus Email'].astype(str)
    df['Card ID Number'] = df['Card ID Number'].astype(str)

    # Merge with the consolidated DataFrame
    consolidated_df = pd.merge(consolidated_df, df, on=['Full Name', 'Campus Email', 'Card ID Number'], how='outer')

    if event_name not in consolidated_df.columns:
        consolidated_df[event_name] = 0
    # Fill NaN values with 0 (indicating absence)
    consolidated_df[event_name] = consolidated_df[event_name].fillna(0).astype(int)

    return consolidated_df

# Main function to consolidate all input files
def consolidate_attendance(input_folder, output_file):
    # Initialize an empty DataFrame with the necessary columns
    consolidated_df = pd.DataFrame(columns=['Full Name', 'Campus Email', 'Card ID Number'])

    # Process each file in the input folder
    for file_name in os.listdir(input_folder):
        if file_name.endswith('.csv'):  # Check for Excel and CSV files
            file_path = os.path.join(input_folder, file_name)
            consolidated_df = process_file(file_path, consolidated_df)
    
    # Save the consolidated DataFrame to an Excel file
    consolidated_df.to_excel(output_file, index=False)

# Define the input folder and output file
input_folder = 'files'  # Folder where the attendance files are stored
output_file = 'consolidated_attendance.xlsx'  # Output file name

# Run the consolidation process
consolidate_attendance(input_folder, output_file)

print(f"Consolidation complete. Output saved to {output_file}.")
