import requests
import pandas as pd

response = requests.post('https://fbrapi.com/generate_api_key')
api_key = response.json()['api_key']

url = "https://fbrapi.com/countries"
headers = {"X-API-Key": api_key}


response = requests.get(url, headers=headers, timeout=30)
data = response.json()["data"]
df = pd.DataFrame(data)
df = df.rename(columns={
    "#_clubs": "clubs",
    "#_players": "players"
})

df.to_csv("./data/countries.csv", index = False, encoding = "utf-8")

