# NBA Attendance Analysis: Market Performance Relative to Arena Capacity

## Business Question
Which NBA franchises are over- or underperforming relative to their arena's capacity, and how has that performance changed over time?

## Data Sources
- **Attendance data**: Scraped from ESPN's NBA attendance reports (2018-2025 seasons), including home/away game averages
- **Arena data**: Scraped from Wikipedia's List of NBA Arenas, including current capacity per team
- **Historical arena data**: Manually added for the Golden State Warriors (Oracle Arena, through 2019) and Los Angeles Clippers (Crypto.com Arena, through 2024), both of whom relocated during the dataset's time range


## Key Findings

**Most teams operate near or above capacity.** Average home attendance rate across all 30 teams was 95.8%, ranging from 83.1% (Washington Wizards) to 104.2% (Dallas Mavericks). Six teams (Cleveland, Milwaukee, Dallas, Philadelphia, Boston, Miami) averaged attendance above their arena's listed capacity, likely reflecting standing-room or floor seating not counted in the official figure.

**Attendance volatility closely tracks competitive volatility, not market size.** The five most volatile teams (Sacramento, San Antonio, Orlando, Oklahoma City, Indiana — all averaging 6-8.6% swing per season) each underwent a significant on-court turnaround during this period. Sacramento is the clearest case: the franchise broke a 16-season playoff drought in 2022-23, then fell back to a play-in-level team the following two seasons — a trajectory that shows up directly in their attendance data as the highest volatility in the league (8.57%).

**High attendance and low volatility can coexist even through real competitive swings.** The Dallas Mavericks posted the highest average attendance rate in the dataset (104.2%) while ranking near the bottom in volatility (1.16%) — despite a stretch that included a Western Conference Finals run, a lottery-bound season, and an NBA Finals appearance. This suggests attendance in some markets is largely decoupled from short-term competitive results, though confirming why (fanbase loyalty, corporate ticket bases, local market strength) would require additional data this project doesn't currently include.

**Golden State's sold-out streak is a genuine outlier.** The Warriors posted exactly 100.00% attendance, 0.00% trend, and 0.00% volatility across every season in the dataset — including a full arena relocation from Oracle Arena (19,596 capacity) to Chase Center (18,064 capacity) in 2019. Demand held at capacity through a change in venue, roster turnover, and years of shifting competitive standing, suggesting a genuinely saturated market rather than a typical demand curve.


## Data Quality Decisions

- **Excluded the 2019-20 and 2020-21 seasons.** The 2019-20 season was suspended mid-year and resumed in a fan-free "bubble" environment; 2020-21 was played on a shortened 72-game schedule with restricted attendance. Both would distort attendance-based comparisons, so they were excluded at query time (not removed from the underlying data).

- **Used home attendance only, not combined home/away.** Away attendance reflects the *host* market's draw, not the visiting team's — including it would blend 29 other cities' attendance patterns into each team's own performance metric.

- **Dropped ESPN's capacity-percentage columns.** ESPN's displayed PCT columns returned corrupted values at the source (e.g. "8884.2"), likely from a hidden sort-key value bleeding into the parsed text. Rather than attempt to repair this, attendance percentage was recalculated directly from average attendance ÷ arena capacity once joined with verified arena data.

- **Manually tracked two mid-dataset arena relocations.** The Golden State Warriors (Oracle Arena → Chase Center, 2019) and Los Angeles Clippers (Crypto.com Arena → Intuit Dome, 2024) both changed venues during this period. The schema tracks arena capacity with a valid season range per arena, so each attendance record joins to the correct arena for that specific season rather than applying a team's current arena capacity retroactively to past seasons.

## Limitations

- **Small sample size for volatility metrics.** Six seasons per team is enough to identify a real signal, but a single unusual season can meaningfully swing a team's volatility ranking — this analysis would benefit from a longer time horizon.

- **No metro population data.** This analysis measures attendance relative to *arena capacity*, not relative to *market size*. A team with a small arena in a large metro area and a team with a large arena in a small metro area could show similar attendance rates despite very different underlying market strength. A genuine market-size comparison would require Census/metro population data layered in.

- **Attendance figures rely on ESPN's reporting**, which is generally understood to reflect tickets distributed rather than verified physical turnstile counts — a standard industry convention, but worth noting as a data provenance caveat.

- **No ticket pricing data.** A team could maintain high attendance through aggressive discounting rather than genuine demand; this analysis can't distinguish between the two.

## Next Steps

- Bring in metro population data to test whether market size, rather than arena capacity alone, better explains attendance patterns

- Layer in team win-loss records directly (rather than researched anecdotally) to formally test the hypothesis that attendance volatility correlates with competitive volatility

- Extend the time range as more seasons become available, to test whether current volatility rankings hold up over a longer horizon


## Technical Approach

**Data pipeline:** Python scrapers pull attendance data from ESPN and arena data from Wikipedia, using `pandas.read_html()` with custom request headers where sites required them. Raw scraped data is preserved separately from cleaned/processed versions at every stage.

**Database design:** Normalized PostgreSQL schema across 3 tables:
- `teams` — one row per franchise, used as the canonical reference to reconcile inconsistent team-name spellings between ESPN and Wikipedia (e.g. "NY Knicks" vs. "New York Knicks")
- `arenas` — one row per arena *era* per team, not one row per team, using `season_start`/`season_end` to correctly track the Warriors' and Clippers' arena relocations rather than applying a single current capacity across the whole dataset
- `team_season_attendance` — one row per team per season, using a composite primary key (`team_id`, `season`)

**Analysis:** Four business questions answered via separate, numbered SQL files, built on a shared reusable view (`rates_with_lag`) combining:
- `LAG()` with `PARTITION BY`/`ORDER BY` to calculate season-over-season change per team
- `FIRST_VALUE()`/`LAST_VALUE()` to compare each team's first vs. most recent season — including correctly handling `LAST_VALUE()`'s default window frame behavior, which otherwise returns a running value instead of the true partition-wide last value
- Standard aggregation (`AVG()`, `GROUP BY`) layered on top of the window-function results in a separate query stage, since window functions and `GROUP BY` can't be combined in a single `SELECT` without a conflict in what the output rows represent
