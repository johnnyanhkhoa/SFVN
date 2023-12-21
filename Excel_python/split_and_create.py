import os
import pandas as pd

# Load the large file into a DataFrame
large_file_path = 'samples/Main File for Splitting.csv'
df = pd.read_csv(large_file_path)

# Print column names for debugging
print(df.columns)

# Create a new folder if it doesn't exist
output_folder = 'new_files'
os.makedirs(output_folder, exist_ok=True)

# Iterate over unique combinations of values in columns CCC and eee
for (value_c, value_d), group_df in df.groupby(['CCC', 'eee']):
    # Create a filename based on values in columns CCC and eee
    filename = f'{output_folder}/output_{value_c}_{value_d}.csv'
    
    # Save the group DataFrame to the corresponding file
    group_df.to_csv(filename, index=False)
    
    print(f"File '{filename}' created with {len(group_df)} rows.")
