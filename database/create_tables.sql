CREATE TABLE episodes (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    broadcast_date DATE NOT NULL
);

CREATE TABLE colors (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE subjects (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE episode_colors (
    episode_id INTEGER REFERENCES episodes(id),
    color_id INTEGER REFERENCES colors(id),
    PRIMARY KEY (episode_id, color_id)
);

CREATE TABLE episode_subjects (
    episode_id INTEGER REFERENCES episodes(id),
    subject_id INTEGER REFERENCES subjects(id),
    PRIMARY KEY (episode_id, subject_id)
);