import requests
import pandas as pd
import time
from openpyxl import load_workbook
import os

#SHEET NAME = LEAGUE ID

response = requests.post('https://fbrapi.com/generate_api_key')
api_key = response.json()['api_key']
headers = {"X-API-Key" : api_key}
url = "https://fbrapi.com/league-seasons"

df_countries = pd.read_excel("./data/countries.xlsx")
country_codes = df_countries['country_code'].tolist()

league_ids_s = []

for code in country_codes:
  df_leagues = pd.read_excel("./data/leagues.xlsx", sheet_name = code, usecols=[1])
  if not df_leagues.empty:
    league_ids_f = df_leagues.iloc[:, 0].tolist() 
    league_ids_s.append(league_ids_f)
  league_ids_r = [x for sublist in league_ids_s for x in sublist]

league_ids = list(set(league_ids_r))
league_ids.sort()
  
for id in league_ids:

  params = {"league_id" : id}

  response = requests.get(url, headers=headers, params=params, timeout=30)
  time.sleep(4)

  data = response.json().get("data", [])
  df = pd.json_normalize(data, sep="_") if data else pd.DataFrame()

  excel_path = "./data/league-seasons.xlsx"
  if not os.path.exists(excel_path):
    pd.DataFrame().to_excel(excel_path, index=False)

  if not df.empty:
    with pd.ExcelWriter("./data/league-seasons.xlsx", mode="a", engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name=str(id), index=False)

wb = load_workbook("./data/league-seasons.xlsx")
std = wb['Sheet1']
wb.remove(std)
wb.save(excel_path)