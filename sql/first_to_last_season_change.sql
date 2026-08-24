SELECT
team_name,
first_season_home_avg,
last_season_home_avg,
(last_season_home_avg - first_season_home_avg) AS first_to_last_difference
FROM rates_with_lag
GROUP BY team_name, last_season_home_avg, first_season_home_avg
ORDER BY first_to_last_difference DESC;
