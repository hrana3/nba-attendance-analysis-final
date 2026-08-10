import pandas as pd

arenas_df = pd.read_csv('data/processed/nba_arenas_clean.csv')

teams = pd.DataFrame({'team_name': arenas_df['Team'].unique()})
teams.to_csv('data/processed/teams.csv', index=False)

print(teams)