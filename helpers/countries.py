import requests
import pandas as pd
import time

response = requests.post('https://fbrapi.com/generate_api_key')
api_key = response.json()['api_key']

url = "https://fbrapi.com/countries"
headers = {"X-API-Key": api_key}

response = requests.get(url, headers=headers, timeout=30)

time.sleep(4)

data = response.json()["data"] if response.status_code == 200 else (print(f"Status: {response.status_code}, Response: {response.text}") or None)

df = pd.DataFrame(data)
df = df.rename(columns={
    "#_clubs": "clubs",
    "#_players": "players"
})

df.to_excel("./data/countries.xlsx", sheet_name="countries", index = False)

