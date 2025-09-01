import requests
import pandas as pd
import time

# API key oluştur
response = requests.post('https://fbrapi.com/generate_api_key')
api_key = response.json()['api_key']
headers = {"X-API-Key": api_key}

# Endpoint URL
url = "https://fbrapi.com/team"  # team endpoint

# Excel’den çekilecek takım listesi (team_id ve season_id içermeli)
df_teams = pd.read_excel('./data/teams.xlsx')

team_ids = df_teams['team_id'].tolist()
season_ids = df_teams['season_id'].tolist()

all_dfs = []

for team_id, season_id in zip(team_ids, season_ids):
    print(f"Processing team_id=NaN, season_id={season_id}")
    
    params = {
        "season_id": season_id
    }
    
    response = requests.get(url, headers=headers, params=params, timeout=30)
    time.sleep(6)
    
    data = response.json()
  
    roster_data = data.get("team_roster", {}).get("data", [])
    df_roster = pd.json_normalize(roster_data, sep="_", max_level=3) if roster_data else pd.DataFrame()
    
    if not df_roster.empty:
        df_roster["team_id"] = team_id
        df_roster["season_id"] = season_id

        list_columns = [col for col in df_roster.columns if df_roster[col].apply(lambda x: isinstance(x, list)).any()]
        for col in list_columns:
            df_roster = df_roster.explode(col).reset_index(drop=True)
            dict_rows = pd.json_normalize(df_roster[col])
            df_roster = df_roster.drop(columns=[col]).join(dict_rows)
        
        all_dfs.append(df_roster)
    
    schedule_data = data.get("team_schedule", {}).get("data", [])
    df_schedule = pd.json_normalize(schedule_data, sep="_", max_level=3) if schedule_data else pd.DataFrame()
    
    if not df_schedule.empty:
        df_schedule["team_id"] = team_id
        df_schedule["season_id"] = season_id
        all_dfs.append(df_schedule)
    
    print(f"team_id={team_id}, season_id={season_id} processed")

excel_path = "./data/team_data.xlsx"
if all_dfs:
    final_df = pd.concat(all_dfs, ignore_index=True)
    final_df.to_excel(excel_path, sheet_name="details", index=False)
