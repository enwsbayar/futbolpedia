import requests
import pandas as pd
import time

response = requests.post('https://fbrapi.com/generate_api_key')
api_key = response.json()['api_key']
headers = {"X-API-Key": api_key}
url = "https://fbrapi.com/league-season-details"

df_league_seasons = pd.read_excel('./data/league_seasons.xlsx')

league_ids = df_league_seasons['league_id'].tolist()
season_ids = df_league_seasons['season_id'].tolist()

all_dfs = []

for league_id, season_id in zip(league_ids, season_ids):

    print(f"Processing league_id={league_id}, season_id={season_id}")
    
    params = {"league_id": int(league_id),
              "season_id": season_id}
    response = requests.get(url, headers=headers, params=params, timeout=30)
    time.sleep(6)

    data = response.json().get("data") if response.status_code == 200 else (print(f"Status: {response.status_code}, Response: {response.text}") or None)
    df = pd.json_normalize(data) if data else pd.DataFrame()

    if not df.empty:
        df["league_id"] = league_id
        df["season_id"] = season_id
        all_dfs.append(df)
    
    print(f"league_id={league_id}, season_id={season_id} processed")

excel_path = "./data/league_season_details.xlsx"

if all_dfs:
    final_df = pd.concat(all_dfs, ignore_index=True)
    final_df.to_excel(excel_path, sheet_name="details", index=False)
