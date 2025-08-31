import requests
import pandas as pd
import time

excel_path = "./data/leagues.xlsx"

response = requests.post('https://fbrapi.com/generate_api_key')
api_key = response.json()['api_key']
headers = {"X-API-Key": api_key}
url = "https://fbrapi.com/leagues"

df_countries = pd.read_excel("./data/countries.xlsx")
country_codes = df_countries['country_code'].tolist()

all_dfs = []

for code in country_codes:
    print(code)
    params = {"country_code": code}
    response = requests.get(url, headers=headers, params=params, timeout=30)
    time.sleep(6)

    data = response.json().get("data", [])
    flat_list = []

    for item in data:
        print(f"Processing {code}")
        league_type = item.get("league_type", "unknown")
        for league in item.get("leagues", []):
            flat_list.append({
                "country_code": code,
                "league_type": league_type,
                "league_id": league.get("league_id"),
                "competition_name": league.get("competition_name"),
                "gender": league.get("gender")
            })

    if flat_list:  
        df = pd.DataFrame(flat_list)
        all_dfs.append(df)

if all_dfs:
    final_df = pd.concat(all_dfs, ignore_index=True)
    final_df.to_excel(excel_path, sheet_name="all_leagues", index=False)
