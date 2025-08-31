import requests
import pandas as pd
import time
import os

response = requests.post('https://fbrapi.com/generate_api_key')
api_key = response.json()['api_key']
headers = {"X-API-Key": api_key}
url = "https://fbrapi.com/league-seasons"

league_ids = []
df_leagues = pd.read_excel('./data/leagues.xlsx')

for idx, row in df_leagues.iterrows():
    league_ids.append(row['league_id'])

u_league_ids = list(set(league_ids))
u_s_league_ids = sorted(u_league_ids)
print(u_s_league_ids)