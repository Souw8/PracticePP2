CREATE TABLE IF NOT EXISTS groups (
    id SERIAL PRIMARY KEY,
    names VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS contacts (
    id SERIAL PRIMARY KEY,
    names VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(100),
    birthday DATE,
    group_id INTEGER REFERENCES groups(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS phones(
    id SERIAL PRIMARY KEY,
    contact_id INTEGER REFERENCES contacts(id) ON DELETE CASCADE,
    phone VARCHAR(20) UNIQUE NOT NULL,
    types VARCHAR(10) CHECK(types IN ('home','work','mobile'))
);

INSERT INTO groups(names)
VALUES ('Family'),('Work'),('Friend'),('Other')
ON CONFLICT (names) DO NOTHING;