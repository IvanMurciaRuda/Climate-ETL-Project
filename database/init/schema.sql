SELECT 'CREATE DATABASE weather_db'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'weather_db')\gexec

\c weather_db

CREATE TABLE IF NOT EXISTS cities (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    latitude DECIMAL (9,6) NOT NULL,
    longitude DECIMAL (9,6) NOT NULL,
    country VARCHAR (100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS weather_raw (
    id SERIAL PRIMARY KEY,
    city_id INT REFERENCES cities (id) ON DELETE CASCADE,
    data JSONB NOT NULL,
    extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS weather_processed (
    id SERIAL PRIMARY KEY,
    city_id INT REFERENCES cities(id) ON DELETE CASCADE,
    weather_date DATE NOT NULL,
    weather_hour INT NOT NULL CHECK (weather_hour >= 0 AND weather_hour <= 23), 
    date_hour TIMESTAMP NOT NULL,
    temperature DECIMAL (5,2),
    humidity INT,
    precipitation DECIMAL(6,2),
    feels_like_temperature DECIMAL (5,2),
    wind_speed DECIMAL (5,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (city_id, weather_date, weather_hour)
);

-- Sample data -- 
INSERT INTO cities (name, latitude, longitude, country) VALUES
('Madrid', 40.4168, -3.7038, 'Spain'),
('Barcelona', 41.3874, 2.1686, 'Spain'),
('Paris', 48.8566, 2.3522, 'France'),
('London', 51.5074, -0.1278, 'UK'),
('Reykjavik', 64.1466, -21.9426, 'Iceland'),
('Rome', 41.9028, 12.4964, 'Italy');