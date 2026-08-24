SELECT t.team_name, a.arena_name, a.capacity, a.season_start, a.season_end, ts.season, ts.all_avg
FROM team_season_attendance ts
JOIN teams t ON ts.team_id = t.team_id
JOIN arenas a ON ts.team_id = a.team_id
WHERE t.team_name = 'Golden State Warriors'
  AND (ts.season BETWEEN COALESCE(a.season_start, 0) AND COALESCE(a.season_end, 9999))
ORDER BY ts.season;


