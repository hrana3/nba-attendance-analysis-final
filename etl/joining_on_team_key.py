import pandas as pd

team_ids = pd.read_csv('data/processed/team_ids.csv')
arenas_df = pd.read_csv('data/processed/nba_arenas_clean.csv')
espn_df = pd.read_csv('data/processed/espn_attendance_processed.csv')

def add_historical_arenas(arenas_df):
    # TODO 2: build the two historical rows as a small DataFrame
    historical_arenas = pd.DataFrame([
    {"Team": "Golden State Warriors", "Arena": "Oracle Arena", "Capacity": 19596, "season_start": None, "season_end": 2019},
    {"Team": "Los Angeles Clippers", "Arena": "Crypto.com Arena", "Capacity": 18997, "season_start": None, "season_end": 2024},
])

# TODO 3: append the historical rows onto arenas_df
# hint: pd.concat() again, same tool you used to combine ESPN's 8 years together
    arenas_df = pd.concat([arenas_df, historical_arenas], ignore_index=True)

    return arenas_df

def build_final_arenas_table(arenas_df, team_ids):
    arenas_df = add_historical_arenas(arenas_df)
    merged_arenas = pd.merge(arenas_df, team_ids, left_on='Team', right_on='team_name')
    merged_arenas =merged_arenas.drop(columns=['Opened','Location','Team','Season of first NBA game','team_name'])
    merged_arenas = merged_arenas.rename(columns={
        'Arena' : 'arena_name',
        'Capacity' : 'capacity'
    })

    return merged_arenas

def build_final_espn_table(espn_df, team_ids):
    merged_espn = pd.merge(espn_df, team_ids, left_on='TEAM', right_on='team_name')
    merged_espn =merged_espn.drop(columns=['RK','TEAM','team_name'])
    merged_espn.columns = merged_espn.columns.str.lower()
    return merged_espn

merged_arenas = build_final_arenas_table(arenas_df, team_ids)
merged_espn = build_final_espn_table(espn_df, team_ids)
#convert floating point type to integer to address type error in psql
merged_arenas['season_start'] = merged_arenas['season_start'].astype('Int64')
merged_arenas['season_end'] = merged_arenas['season_end'].astype('Int64')
arenas_final = merged_arenas.to_csv('data/processed/arenas_final.csv', index=False)
espn_final = merged_espn.to_csv('data/processed/espn_final.csv', index=False)
#print(merged_espn.head(40))
#print(len(espn_df), len(merged_espn))
#print(merged_arenas['team_id'].isna().sum())
#print(merged_arenas.columns.tolist())
#print(merged_espn.columns.tolist())