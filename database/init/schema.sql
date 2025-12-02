SELECT 'CREATE DATABASE weather_db'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'weather_db')\gexec

\c weather_db

CREATE TABLE cities (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    latitude DECIMAL (9,6) NOT NULL,
    longitude DECIMAL (9,6) NOT NULL,
    country VARCHAR (100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE weather_raw (
    id SERIAL PRIMARY KEY,
    city_id INT REFERENCES cities (id) ON DELETE CASCADE,
    data JSONB NOT NULL,
    extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP    
);

-- Sample data -- 
INSERT INTO cities (name, latitude, longitude, country) VALUES
('Madrid', 40.4168, -3.7038, 'Spain'),
('Barcelona', 41.3874, 2.1686, 'Spain');