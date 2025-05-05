import pandas as pd
import json

# URL to the raw JSON file on GitHub
url = "https://github.com/odilbekmarimov/DemoProject/raw/main/column_table_map.json"

# Load the JSON file into a DataFrame using pandas
df = pd.read_json(url)

output_file = "column_table_map.json"
df.to_json(output_file, orient="records")

print(f"\nDataFrame saved in pretty format as '{output_file}'")

# Define a dictionary with file names and corresponding URLs from GitHub
files_urls = {
    "t01.csv": "https://raw.githubusercontent.com/odilbekmarimov/DemoProject/main/files_final/t01.csv",
    "t02.csv": "https://raw.githubusercontent.com/odilbekmarimov/DemoProject/main/files_final/t02.csv",
    "t03.csv": "https://raw.githubusercontent.com/odilbekmarimov/DemoProject/main/files_final/t03.csv",
    "t04.csv": "https://raw.githubusercontent.com/odilbekmarimov/DemoProject/main/files_final/t04.csv",
    "t05.csv": "https://raw.githubusercontent.com/odilbekmarimov/DemoProject/main/files_final/t05.csv",
    "t07.csv": "https://raw.githubusercontent.com/odilbekmarimov/DemoProject/main/files_final/t07.csv"
}

# Download and save the CSV files excluding t06.csv
for file_name, url in files_urls.items():
    if file_name != "t06.csv":
        df = pd.read_csv(url)
        local_filename = f"{file_name}"
        df.to_csv(local_filename, index=False)
        print(f"CSV file '{file_name}' saved as '{local_filename}'")

