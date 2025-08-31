import requests
import pandas as pd
import time
import os

response = requests.post('https://fbrapi.com/generate_api_key')
api_key = response.json()['api_key']
headers = {"X-API-Key": api_key}
url = "https://fbrapi.com/league-seasons"

df_leagues = pd.read_excel('./data/leagues.xlsx')

league_ids = df_leagues['league_id'].tolist()

u_league_ids = list(set(league_ids))
u_s_league_ids = sorted(u_league_ids)

all_dfs = []

for id in u_s_league_ids:
    print(f"Processing league_id = {id}")
    params = {"league_id": {id}}
    response = requests.get(url, headers=headers, params=params, timeout=30)
    time.sleep(6)

    data = response.json().get("data", [])
    df = pd.json_normalize(data, sep="_") if data else pd.DataFrame()
    print(data)

    if not df.empty:
        df.insert(0, "league_id", [id] * len(df))
        all_dfs.append(df)

    print(f"league_id = {id} processed" )

excel_path = "./data/league_seasons.xlsx"
if all_dfs:
    final_df = pd.concat(all_dfs, ignore_index=True)
    final_df.to_excel(excel_path, sheet_name="league_seasons", index=False)
