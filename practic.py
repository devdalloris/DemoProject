import pandas as pd
import json
with open("column_table_map.json", "r") as file:
    mappings = json.load(file)

# Iterate through the mappings for each table
for table_mapping in mappings:
    table_name = table_mapping.get("01")  # Get the table name
    file_name = table_mapping.get("01")  # Get the file name

    # Load the table data into a DataFrame
    df = pd.read_csv(f"{file_name}.csv")

    # Get the column mappings for the current table
    column_mapping = mappings[-1].get(file_name)

    # Rename the columns in the DataFrame
    df = df.rename(columns=column_mapping)

    # Save the updated DataFrame back to a new CSV file
    df.to_csv(f"{file_name}_updated.csv", index=False)

    print(f"Columns renamed and saved for table {table_name} ({file_name})")

print("All tables updated and saved.")