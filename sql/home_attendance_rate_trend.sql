--Avg attendance rate trend per team from 2018-2025

SELECT
team_name,
AVG((attendance_rate - prev_attendance_rate)) AS avg_attendance_rate_2018_to_2025
FROM rates_with_lag
GROUP BY team_name
ORDER BY avg_attendance_rate_2018_to_2025 DESC;