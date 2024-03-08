import pandas as pd
import os 

print("Current Working Directory: ", os.getcwd())


csv_files = ['./register_maps/fronius_information.csv', './register_maps/fronius_capability.csv', './register_maps/fronius_settings.csv']

#Read each CSV file into a DataFrame and store them in a list
dataframes = [pd.read_csv(file) for file in csv_files]

# Step 2: Concatenate all DataFrames into a single DataFrame
combined_df = pd.concat(dataframes, ignore_index=True)

# Remove fields from the DataFrame
combined_df.drop(columns=['Description'], inplace=True)
combined_df.drop(columns=['Fronius_Field_Name'], inplace=True)

# Print all database fields (column names)
print(combined_df.columns.tolist())

# Display the entire DataFrame
print("\nComplete DataFrame:")
print(combined_df)

# Get mapping information by RDS field name from the combined DataFrame
def get_mapping_by_rds_field(df, rds_field_name):
    """
    Retrieve mapping information for a given RDS field name from the DataFrame.
    
    Parameters:
    - df: Combined DataFrame containing the DER to register mapping from multiple CSV files.
    - rds_field_name: The RDS field name to retrieve mapping for.
    
    Returns:
    - DataFrame with the mapping information for the specified RDS field.
    """
    mapping = df[df['RDS Fields'] == rds_field_name]
    return mapping

# Example usage of the function for specific mapping inquiries
rds_field_name = 'der_name'  # Example: Retrieve mapping for 'der_name'
mapping_info = get_mapping_by_rds_field(combined_df, rds_field_name)

# If you still want to display specific mapping information
print("\nSpecific Mapping Information for RDS Field Name '{}':".format(rds_field_name))
print(mapping_info)
