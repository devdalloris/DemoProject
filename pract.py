import pandas as pd
import json

# Load the JSON mapping from 'p.json'
try:
    data_json = {
        "01": {
            "table": "users",
            "file": "t01.csv",
            "prefix": "01-XX",
            "columns": {
                "00": "id",
                "01": "name",
                "02": "phone_number",
                "03": "email",
                "04": "created_at",
                "05": "last_active_at",
                "07": "is_vip",
                "08": "total_balance"
            }
        },
        "02": {
            "table": "cards",
            "file": "t02.csv",
            "prefix": "02-XX",
            "columns": {
                "00": "id",
                "01": "user_id",
                "02": "card_number",
                "03": "balance",
                "05": "created_at",
                "06": "card_type",
                "07": "limit_amount"
            }
        }
    }
except FileNotFoundError:
    print("Error: 'p.json' file not found.")
    exit()
except json.JSONDecodeError:
    print("Error: Invalid JSON format in 'p.json'.")
    exit()

# Assuming you want to process the 't01.csv' file based on the "01" key in the JSON
mapping_01 = data_json.get("01")

if mapping_01:
    input_filename = mapping_01.get("file")
    column_rename_map = mapping_01.get("columns")

    if input_filename == 't01.csv' and column_rename_map:
        try:
            # Read the CSV file 't01.csv' without a header
            df = pd.read_csv(input_filename, header=None)

            # Create a new list of column names based on the mapping
            new_columns = []
            for i in range(len(df.columns)):
                column_index_str = str(i).zfill(2)  # Format index as two-digit string
                if column_index_str in column_rename_map:
                    new_columns.append(column_rename_map[column_index_str])
                else:
                    # If a column index is not in the mapping, keep a default name
                    new_columns.append(f"unknown_{i}")

            # Assign the new column names to the DataFrame
            df.columns = new_columns

            # Print the DataFrame with the new column names
            print("DataFrame with renamed columns:")
            print(df.head())

            # If you want to save the changes to a new CSV file (e.g., 'users.csv'):
            output_filename = mapping_01.get("table") + ".csv"
            df.to_csv(output_filename, index=False)
            print(f"\nDataFrame saved to '{output_filename}' with renamed columns.")

        except FileNotFoundError:
            print(f"Error: CSV file '{input_filename}' not found.")
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        print("Error: Could not find mapping for 't01.csv' or 'columns' in 'p.json' under the '01' key.")
else:
    print("Error: Key '01' not found in 'p.json'.")