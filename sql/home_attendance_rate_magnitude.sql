SELECT
team_name,
AVG(ABS((attendance_rate - prev_attendance_rate))) AS avg_attendance_magnitude_2018_to_2025
FROM rates_with_lag
GROUP BY team_name
ORDER BY avg_attendance_magnitude_2018_to_2025 DESC;