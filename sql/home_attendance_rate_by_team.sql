--attendance by team

SELECT t.team_name,
AVG((ts.home_avg::NUMERIC /a.capacity)) *100 AS attendance_rate
FROM team_season_attendance ts
JOIN teams t ON ts.team_id = t.team_id
JOIN arenas a ON ts.team_id = a.team_id
    AND (ts.season BETWEEN COALESCE(a.season_start,0) AND COALESCE(a.season_end, 9999))
WHERE ts.season NOT IN (2020,2021)
GROUP BY t.team_name
ORDER BY attendance_rate DESC;
