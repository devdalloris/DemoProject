import pandas as pd
import json

base_url = 'https://raw.githubusercontent.com/odilbekmarimov/DemoProject/main/column_table_map.json'

url = [
    'https://raw.githubusercontent.com/odilbekmarimov/DemoProject/main/files_final/t01.csv',
    'https://raw.githubusercontent.com/odilbekmarimov/DemoProject/main/files_final/t02.csv',
    'https://raw.githubusercontent.com/odilbekmarimov/DemoProject/main/files_final/t03.csv',
    'https://raw.githubusercontent.com/odilbekmarimov/DemoProject/main/files_final/t04.csv',
    'https://raw.githubusercontent.com/odilbekmarimov/DemoProject/main/files_final/t05.csv',
    'https://raw.githubusercontent.com/odilbekmarimov/DemoProject/main/files_final/t07.csv'
]

try:
    df_map = pd.read_json(base_url)
    print("Content of column_table_map.json:")
    print(df_map)

    # Save the JSON DataFrame to a local JSON file
    df_map.to_json('column_table_map_saved.json')
    print("\ncolumn_table_map.json saved to column_table_map_saved.json")

    for i, csv_url in enumerate(url):
        # Construct the key to look up in the JSON map
        table_key = f"0{i+1}" if i < 9 else f"{i+1}"

        if table_key in df_map:
            mapping_data = df_map[table_key]
            print(f"\nProcessing file: {csv_url} with mapping data: {mapping_data}")

            if 'columns' in mapping_data:
                column_mapping = mapping_data['columns']

                # Read the CSV file
                df_csv = pd.read_csv(csv_url)
                print("\nOriginal CSV data:")
                print(df_csv.head())  # Print the first few rows

                # Create a new list of column names based on the mapping
                new_columns = [None] * len(df_csv.columns)  # Initialize with None

                for original_index_str, new_column_name in column_mapping.items():
                    try:
                        original_index = int(original_index_str)
                        if 0 <= original_index < len(new_columns):
                            new_columns[original_index] = new_column_name
                        else:
                            print(f"Warning: Invalid original column index '{original_index_str}' in mapping for {csv_url}.")
                    except ValueError:
                        print(f"Warning: Invalid original column index format '{original_index_str}' in mapping for {csv_url}.")

                # Check if all new column names are assigned
                if all(name is not None for name in new_columns):
                    # Rename the columns
                    df_csv.columns = new_columns
                    print("\nCSV data with renamed columns:")
                    print(df_csv.head())  # Print the first few rows

                    # Save the modified DataFrame to a new CSV file
                    output_filename = f"modified_t{i+1}.csv"
                    df_csv.to_csv(output_filename, index=False)
                    print(f"\nModified data saved to {output_filename}")
                else:
                    print(f"\nError: Incomplete column mapping in column_table_map.json for {csv_url}. Not all columns could be renamed.")

            else:
                print(f"\nWarning: 'columns' key not found in mapping for {csv_url}. Skipping renaming.")

        else:
            print(f"\nWarning: Key '{table_key}' not found in column_table_map.json for file: {csv_url}. Skipping.")

except Exception as e:
    print(f"An error occurred: {e}")
    print("Please ensure the URLs are correct and the JSON file has the expected structure.")