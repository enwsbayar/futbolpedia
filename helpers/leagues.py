import requests
import pandas as pd
import time

response = requests.post('https://fbrapi.com/generate_api_key')
api_key = response.json()['api_key']
headers = {"X-API-Key": api_key}
url = "https://fbrapi.com/leagues"

df_countries = pd.read_excel("./data/countries.xlsx")
country_codes = df_countries['country_code'].tolist()

with pd.ExcelWriter("./data/leagues.xlsx", engine="xlsxwriter") as writer:

    for code in country_codes:
        params = {"country_code": code}

        response = requests.get(url, headers=headers, params=params, timeout=30)
        time.sleep(3)  

        data = response.json().get("data", [])
        print(data)
        flat_list = []

        for item in data:
            league_type = item.get("league_type", "unknown")
            for league in item.get("leagues", []):
                flat_list.append({
                    "league_type": league_type,
                    "league_id": league.get("league_id"),
                    "competition_name": league.get("competition_name"),
                    "gender": league.get("gender")
                })
           
       
        df = pd.DataFrame(flat_list)
        df.to_excel(writer, sheet_name=code, index=False)


