import pandas as pd
import requests
import json

# GitHub URLs
json_url = "https://raw.githubusercontent.com/odilbekmarimov/DemoProject/main/column_table_map.json"
base_csv_url = "https://raw.githubusercontent.com/odilbekmarimov/DemoProject/main/files_final/"
csv_files = [f"t0{i}.csv" for i in range(1, 6)] + ["t07.csv"]

renamed_tables = {}

try:
    # Fetch and parse the JSON mapping file
    response = requests.get(json_url)
    response.raise_for_status()  # Raise an exception for bad status codes
    mapping = response.json()

    # Create a table name mapping dictionary using "Table ID" as key
    table_name_mapping = {item["Table ID"]: item["Table Name"]
                          for item in mapping if "Table ID" in item and "Table Name" in item}

    # Create a column name mapping dictionary based on "File Name"
    column_name_mapping = {item["File Name"].replace(".csv", ""): {
        col: f"{item['Column Prefix']}-{col.split('-', 1)[1].lstrip('-')}"
        if "-" in col and "Column Prefix" in item else col
        for col in pd.read_csv(base_csv_url + item["File Name"], nrows=0).columns
    }
                           for item in mapping if "File Name" in item and "Column Prefix" in item}

    for csv_file in csv_files:
        # Construct the raw CSV URL
        csv_url = base_csv_url + csv_file
        original_table_name_short = csv_file.replace(".csv", "")

        # Determine the "Table ID" from the filename (assuming a pattern like 't01' corresponds to '01')
        table_id = original_table_name_short.lstrip("t0").lstrip("t")
        new_table_name = table_name_mapping.get(table_id)

        try:
            # Load the CSV file into a pandas DataFrame
            df = pd.read_csv(csv_url)

            # Rename columns if a mapping exists for this table (using filename as key)
            if original_table_name_short in column_name_mapping:
                df.columns = [column_name_mapping[original_table_name_short].get(col, col) for col in df.columns]

            # Store the renamed DataFrame with the new table name as the key
            if new_table_name:
                renamed_tables[new_table_name] = df
            else:
                renamed_tables[original_table_name_short] = df # Keep original short name if no mapping

            print(f"Processed and renamed: {csv_file} -> {new_table_name if new_table_name else original_table_name_short}")

        except requests.exceptions.RequestException as e:
            print(f"Error fetching CSV file {csv_file}: {e}")
        except pd.errors.EmptyDataError:
            print(f"Warning: CSV file {csv_file} is empty.")
        except Exception as e:
            print(f"An error occurred processing {csv_file}: {e}")

    # Now the 'renamed_tables' dictionary contains the DataFrames with new table and column names
    print("\nSuccessfully processed all files. The renamed DataFrames are stored in the 'renamed_tables' dictionary.")
    # You can now access the DataFrames using their new table names
    # For example:
    # if "users" in renamed_tables:
    #     print(renamed_tables["users"].head())

except requests.exceptions.RequestException as e:
    print(f"Error fetching JSON file: {e}")
except json.JSONDecodeError:
    print("Error decoding the JSON file.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")