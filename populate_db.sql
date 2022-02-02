DROP TABLE IF EXISTS animes;

CREATE TABLE IF NOT EXISTS animes (
    id            BIGSERIAL       PRIMARY KEY,
    anime         VARCHAR(100)    NOT NULL        UNIQUE,
    released_date DATE            NOT NULL,
    seasons       INTEGER         NOT NULL
);