import pandas as pd

espn_df = pd.read_csv('data/processed/espn_attendance_processed.csv')
arenas_df = pd.read_csv('data/processed/nba_arenas_clean.csv')

print(espn_df['TEAM'].unique())
print(arenas_df['Team'].unique())


