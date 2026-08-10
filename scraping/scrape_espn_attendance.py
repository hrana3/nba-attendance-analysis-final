import pandas as pd
import time
import requests
from io import StringIO

def scrape_year(year):
    url = f"https://www.espn.com/nba/attendance/_/year/{year}"
    
    # TODO: use pd.read_html(url) — it returns a LIST of tables found on the page.
    # ESPN's attendance page usually has the data in the first table (index 0),
    # but print len(tables) and inspect tables[0].head() to confirm before assuming.
    tables = pd.read_html(url)
    df = tables[0]
    
    df.to_csv(f"data/raw/espn_{year}_raw.csv", index=False) 
    # TODO: add a column so you know which season each row belongs to
    
    # TODO: drop junk rows — look for rows where TEAM is not a real team name
    # (e.g. 'East', 'West', 'Team Chuck', 'Team Shaq')
    # hint: you could build a list of the 30 real team names and filter with .isin()
      # Keep only rows where TEAM is in your list of real team names
    

# drop whatever junk header rows landed inside the data
    df = df.iloc[2:].reset_index(drop=True)   # adjust the number based on what you see in df.head(10)

    df.columns = ['RK', 'TEAM', 'HOME_GMS', 'HOME_TOTAL', 'HOME_AVG', 'HOME_PCT',
                'ROAD_GMS', 'ROAD_AVG', 'ROAD_PCT', 'ALL_GMS', 'ALL_AVG', 'ALL_PCT']  
    
    df = df.drop(columns=['HOME_PCT', 'ROAD_PCT', 'ALL_PCT'])
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


def scrape_arenas():
    url = "https://en.wikipedia.org/wiki/List_of_NBA_arenas"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Personal portfolio project; contact: hrana3 )"
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()   # will raise an error here if something's still wrong, easier to debug
    
    tables = pd.read_html(StringIO(response.text))
    df = tables[0]
    df.to_csv('data/raw/nba_arenas_raw.csv', index=False) 
    df = df.drop(columns=['Image', 'Ref'])
    df.to_csv('data/processed/nba_arenas_clean.csv', index=False)
    
    print(df.columns.tolist())
    print(df.head(10))
    
    return df

# TODO: once you can see the raw data, figure out how to identify 
# "current" arena rows. Look for a column like "Years used" — 
# current arenas will likely say something like "1999–present" 
# rather than a closed range like "1996–2003".
# Hint: you could filter with df['Years used'].str.contains('present')
# but check the exact wording first, it might be 'Present' or use a 
# different dash character than a normal hyphen.

# TODO: call scrape_multiple_years() for whatever range you decide on,
# then inspect the result before saving — check for the 2025 zero-values
# problem and the broken PCT columns before trusting anything
if __name__ == "__main__":
    all_years = scrape_multiple_years(2018, 2025)
    combined = pd.concat(all_years, ignore_index=True)
    arenas = scrape_arenas()
    
    #print(combined.head())          # quick sanity check in the terminal
    #print(combined.shape)           # how many rows/columns you ended up with
    #print(combined['TEAM'].unique())
    #print(combined['season'].value_counts())
    combined.to_csv("data/processed/espn_attendance_processed.csv", index=False)
    #print("Saved to data/raw/espn_attendance_raw.csv")
    #print(arenas.head())
    #print(arenas.shape())