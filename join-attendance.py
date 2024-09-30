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
    print("df:", df)

    # Collect headers from the DataFrame
    headers = df.columns

    # Check if the event column already exists in the consolidated DataFrame
    if event_name not in consolidated_df.columns:
        # Add the event column with default values (0 for absence)
        consolidated_df[event_name] = 0

    new_row = None
    
    # Iterate over the names of students present in the current file
    for row in df.itertuples(index=False):
        
        # Extract the full name from the row
        row_dict = dict(zip(headers, row))
        #if pd.isna(row_dict['Last Name']) or pd.isna(row_dict['First Name']):
         #       return consolidated_df
        
        full_name = f"{row_dict['First Name']} {row_dict['Last Name']}"
        print("Checking for", full_name)

        if pd.isna(row_dict['First Name']) or pd.isna(row_dict['Last Name']):
            return consolidated_df
        
        # Check if the full name is already present in the consolidated DataFrame
        if full_name in consolidated_df['Full Name'].values:
            print(f"Found {full_name}")
            # Update the attendance for the event
            print("Full Name:", full_name)
            print("Event Name:", event_name)
            print(full_name in consolidated_df['Full Name'].values)
            consolidated_df.loc[consolidated_df['Full Name'] == full_name, event_name] = 1
        else:
            # Create a new row for the student
            print(f"Could not find {full_name}") 
            
            new_row = {
                'Full Name': full_name,
                'Campus Email': row_dict['Campus Email'], 
                'Card ID Number': row_dict['Card ID Number'],  # Replace with appropriate default value
                event_name: 1
            }
            print("New row:", new_row)
            # Append the new row to the DataFrame
            new_row_df = pd.DataFrame([new_row])
            consolidated_df = pd.concat([consolidated_df, new_row_df], ignore_index=True)
        print("Updated:", consolidated_df)

    return consolidated_df

# Main function to consolidate all input files
def consolidate_attendance(input_folder, output_file):
    # Clear the contents of the output file by opening it in write mode
    with open(output_file, 'w') as f:
        pass

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
