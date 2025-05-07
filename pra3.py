import pandas as pd
import json
import requests

base_url = 'https://raw.githubusercontent.com/odilbekmarimov/DemoProject/main/column_table_map.json'

csv_urls = [
    'https://raw.githubusercontent.com/odilbekmarimov/DemoProject/main/files_final/t01.csv',
    'https://raw.githubusercontent.com/odilbekmarimov/DemoProject/main/files_final/t02.csv',
    'https://raw.githubusercontent.com/odilbekmarimov/DemoProject/main/files_final/t03.csv',
    'https://raw.githubusercontent.com/odilbekmarimov/DemoProject/main/files_final/t04.csv',
    'https://raw.githubusercontent.com/odilbekmarimov/DemoProject/main/files_final/t05.csv',
    'https://raw.githubusercontent.com/odilbekmarimov/DemoProject/main/files_final/t07.csv'
]

def rename_columns(df, column_mapping, csv_url):
    """
    Renames the columns of a DataFrame based on a provided mapping.

    Args:
        df (pd.DataFrame): The DataFrame to rename.
        column_mapping (dict): A dictionary mapping original column indices (strings)
            to new column names (strings).
        csv_url (str): The URL of the CSV file (for logging purposes).

    Returns:
        pd.DataFrame: The DataFrame with renamed columns.
    """
    original_columns = df.columns.tolist()
    num_cols = len(original_columns)
    new_columns = list(original_columns)

    print(f"\n[DEBUG] Original columns for {csv_url}: {original_columns}")
    print(f"[DEBUG] Column mapping for {csv_url}: {column_mapping}")

    for original_index_str, new_column_name in column_mapping.items():
        try:
            original_index = int(original_index_str)
            if 0 <= original_index < num_cols:
                new_columns[original_index] = new_column_name
            else:
                print(
                    f"Warning: Invalid original column index '{original_index_str}' in mapping for {csv_url}."
                )
        except ValueError:
            print(
                f"Warning: Invalid original column index format '{original_index_str}' in mapping for {csv_url}."
            )
            return df

    print(f"[DEBUG] New columns for {csv_url}: {new_columns}")
    df.columns = new_columns
    return df


def main():
    """
    Main function to fetch JSON mapping, modify it, read CSV files, and rename columns.
    """
    try:
        # Fetch the JSON data
        response = requests.get(base_url)
        response.raise_for_status()
        json_data = response.json()

        print("Original column_table_map.json:")
        print(json_data)

        # Modify the JSON data for t01.csv
        if "01" in json_data and "columns" in json_data["01"]:
            # Correct the mapping for "06" to be "is_vip"
            json_data["01"]["columns"]["06"] = "is_vip"
            #Correct the mapping for "07" to be "total_balance"
            json_data["01"]["columns"]["07"] = "total_balance"

        # Modify the JSON data for t02.csv
        if "02" in json_data and "columns" in json_data["02"]:
            json_data["02"]["columns"]["04"] = json_data["02"]["columns"].pop("05")
            json_data["02"]["columns"]["05"] = json_data["02"]["columns"].pop("06")
            json_data["02"]["columns"]["06"] = "limit_amount"
        
        print("\nModified column_table_map.json:")
        print(json_data)

        # Convert the modified JSON data to a DataFrame
        df_map = pd.DataFrame(json_data)


        # Save the JSON DataFrame to a local file (for debugging)
        df_map.to_json('column_table_map_saved.json')
        print("\nModified column_table_map.json saved to column_table_map_saved.json")

        for i, csv_url in enumerate(csv_urls):
            table_key = f"0{i+1}" if i < 9 else f"{i+1}"

            if table_key in json_data:
                mapping_data = json_data[table_key]
                print(f"\nProcessing file: {csv_url} with mapping data:\n{mapping_data}")

                if 'columns' in mapping_data:
                    column_mapping = mapping_data['columns']
                    try:
                        # Read the CSV file
                        df_csv = pd.read_csv(csv_url)
                        print("\nOriginal CSV data:")
                        print(df_csv.head())

                        # Rename columns using the helper function
                        df_csv = rename_columns(df_csv, column_mapping, csv_url)

                        print("\nCSV data with renamed columns:")
                        print(df_csv.head())

                        # Save the modified DataFrame to a new CSV file
                        output_filename = f"modified_t{i+1}.csv"
                        df_csv.to_csv(output_filename, index=False)
                        print(f"\nModified data saved to {output_filename}")
                    except Exception as e:
                        print(f"Error processing CSV file: {csv_url}: {e}")
                        continue

                else:
                    print(
                        f"\nWarning: 'columns' key not found in mapping for {csv_url}. Skipping renaming."
                    )
            else:
                print(
                    f"\nWarning: Key '{table_key}' not found in column_table_map.json for file: {csv_url}. Skipping."
                )

    except requests.exceptions.RequestException as e:
        print(f"Error fetching JSON: {e}")
        print(
            "Please ensure the URLs are correct, your internet connection is stable, and the JSON file has the expected structure."
        )
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        print("Please check the code and data files.")



if __name__ == "__main__":
    main()
