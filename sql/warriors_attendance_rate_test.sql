WITH rates AS (
    SELECT t.team_name,
    ts.season,
    (home_avg::NUMERIC / capacity * 100) AS attendance_rate,
    a.capacity, 
    ts.home_avg
    FROM team_season_attendance AS ts
    JOIN teams t ON ts.team_id = t.team_id
    JOIN arenas a ON ts.team_id = a.team_id
        AND (ts.season BETWEEN COALESCE(a.season_start,0) AND COALESCE(a.season_end, 9999))
    WHERE ts.season NOT IN (2020,2021) 
    AND t.team_name = 'Golden State Warriors'
    --GROUP BY t.team_name , ts.season, attendance_rate, a.capacity, ts.home_avg
)

SELECT team_name,
    season,
    attendance_rate,
    LAG(attendance_rate) OVER (
    PARTITION BY team_name
    ORDER BY season
) AS prev_attendance_rate,
    home_avg,
    capacity
    FROM RATES
