-- NBA attendance analysis schema
-- teams: one row per team (canonical names, used to reconcile ESPN/Wikipedia spelling differences)
-- arenas: one row per arena-era per team (handles teams that changed arenas mid-dataset)
-- team_season_attendance: one row per team per season

DROP TABLE IF EXISTS team_season_attendance;
DROP TABLE IF EXISTS arenas;
DROP TABLE IF EXISTS teams;

CREATE TABLE teams (
    team_id    SERIAL PRIMARY KEY,
    team_name  VARCHAR(50) NOT NULL
);

CREATE TABLE arenas (
    arena_id     SERIAL PRIMARY KEY,
    team_id      INT REFERENCES teams(team_id),
    arena_name   VARCHAR(50),
    capacity     INT,
    season_start INT,
    season_end   INT
);

CREATE TABLE team_season_attendance (
    team_id    INT REFERENCES teams(team_id),
    home_gms   INT,
    home_total INT,
    home_avg   INT,
    road_gms   INT,
    road_avg   INT,
    all_gms    INT,
    all_avg    INT,
    season     INT,
    PRIMARY KEY (team_id, season)
);