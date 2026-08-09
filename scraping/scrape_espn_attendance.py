import pandas as pd
import time

def scrape_year(year):
    url = f"https://www.espn.com/nba/attendance/_/year/{year}"
    
    # TODO: use pd.read_html(url) — it returns a LIST of tables found on the page.
    # ESPN's attendance page usually has the data in the first table (index 0),
    # but print len(tables) and inspect tables[0].head() to confirm before assuming.
    tables = pd.read_html(url)
    df = tables[0]
    
    # TODO: add a column so you know which season each row belongs to
    
    # TODO: drop junk rows — look for rows where TEAM is not a real team name
    # (e.g. 'East', 'West', 'Team Chuck', 'Team Shaq')
    # hint: you could build a list of the 30 real team names and filter with .isin()
      # Keep only rows where TEAM is in your list of real team names
    

# drop whatever junk header rows landed inside the data
    df = df.iloc[2:].reset_index(drop=True)   # adjust the number based on what you see in df.head(10)

    df.columns = ['RK', 'TEAM', 'HOME_GMS', 'HOME_TOTAL', 'HOME_AVG', 'HOME_PCT',
                'ROAD_GMS', 'ROAD_AVG', 'ROAD_PCT', 'ALL_GMS', 'ALL_AVG', 'ALL_PCT']  
    df['season'] = year
    # Keep only rows where TEAM is in your list of real team names
    real_teams = ['Bulls', 'Mavericks', '76ers', 'Heat', 'NY Knicks', 'Nuggets', 
                'Raptors', 'Cavaliers', 'Celtics', 'Clippers', 'Lakers', 'Magic',
                'Trail Blazers', 'Jazz', 'Pistons', 'Spurs', 'Warriors', 
                'Timberwolves', 'Kings', 'Bucks', 'Nets', 'Rockets', 'Thunder',
                'Pelicans', 'Suns', 'Hawks', 'Wizards', 'Grizzlies', 'Pacers', 'Hornets']

    df = df[df['TEAM'].isin(real_teams)]
    
    return df

def scrape_multiple_years(start_year, end_year):
    all_years = []
    for year in range(start_year, end_year + 1):
        print(f"Scraping {year}...")
        try:
            df = scrape_year(year)
            all_years.append(df)
        except Exception as e:
            print(f"  Failed on {year}: {e}")
        time.sleep(1)  # be polite to ESPN's server
    
    # TODO: combine all years into one DataFrame with pd.concat()
    return all_years

# TODO: call scrape_multiple_years() for whatever range you decide on,
# then inspect the result before saving — check for the 2025 zero-values
# problem and the broken PCT columns before trusting anything
if __name__ == "__main__":
    all_years = scrape_multiple_years(2018, 2025)
    combined = pd.concat(all_years, ignore_index=True)
    
    print(combined.head())          # quick sanity check in the terminal
    print(combined.shape)           # how many rows/columns you ended up with
    print(combined['TEAM'].unique())
    print(combined['season'].value_counts())
    combined.to_csv("data/raw/espn_attendance_raw.csv", index=False)
    print("Saved to data/raw/espn_attendance_raw.csv")