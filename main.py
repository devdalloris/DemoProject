import pandas as pd
import requests
import json

ctm=pd.read_json('column_table_map.json')
d=ctm["01"]["columns"]

url_to1 = "https://raw.githubusercontent.com/odilbekmarimov/DemoProject/main/files_final/t01.csv"
url_to2 = "https://raw.githubusercontent.com/odilbekmarimov/DemoProject/main/files_final/t02.csv"
url_to3 = "https://raw.githubusercontent.com/odilbekmarimov/DemoProject/main/files_final/t03.csv"
url_to4 = "https://raw.githubusercontent.com/odilbekmarimov/DemoProject/main/files_final/t04.csv"
url_to5 = "https://raw.githubusercontent.com/odilbekmarimov/DemoProject/main/files_final/t05.csv"
url_to7 = "https://raw.githubusercontent.com/odilbekmarimov/DemoProject/main/files_final/t07.csv"

t01 = pd.read_csv(url_to1)




