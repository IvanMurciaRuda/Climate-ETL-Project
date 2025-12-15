import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'airflow', 'plugins'))

from transform import WeatherTransform

class TestWeatherTransform:

    transformer = WeatherTransform()

    def setup(self):
        self.transformer = WeatherTransform()

    #should return a number and should be lower than real temperature
    def test_calculate_feels_like_temperature_cold_mode(self):
        result = self.transformer.calculate_feels_like(5, 80, 10)

        assert isinstance(result, (int, float))
        assert result < 5

    #should return a number and should be higher than real temperature
    def test_calculate_feels_like_temperature_hot_mode(self):
        result = self.transformer.calculate_feels_like(35, 80, 20)

        assert isinstance(result, (int, float))
        assert result > 35
    
    #should return an empty list
    def test_extract_data_with_empty_input(self):
        result = self.transformer.extract_hourly_records([])
        assert result == []

    def test_extract_data_with_real_data(self):
        test_data = [
            {
                "city_id" : 1,
                "latitude": 40.4375,
                "longitude": -3.6875,
                "city_name" : "Madrid",
                "raw_json":{
                    "hourly": {
                        "time": [
                            "2025-12-09T00:00",
                            "2025-12-09T01:00",
                            "2025-12-09T02:00",
                            "2025-12-09T03:00",
                            "2025-12-09T04:00",
                            "2025-12-09T05:00",
                            "2025-12-09T06:00",
                            "2025-12-09T07:00",
                            "2025-12-09T08:00",
                            "2025-12-09T09:00",
                            "2025-12-09T10:00",
                            "2025-12-09T11:00",
                            "2025-12-09T12:00",
                            "2025-12-09T13:00",
                            "2025-12-09T14:00",
                            "2025-12-09T15:00",
                            "2025-12-09T16:00",
                            "2025-12-09T17:00",
                            "2025-12-09T18:00",
                            "2025-12-09T19:00",
                            "2025-12-09T20:00",
                            "2025-12-09T21:00",
                            "2025-12-09T22:00",
                            "2025-12-09T23:00"
                        ],
                        "temperature_2m": [7.7, 6.9, 6.6, 6.3, 5.8, 5.4, 4.8, 4, 3.5, 3.5, 4.7, 6.9, 8.8, 10.4, 11, 11.7, 12.1, 12.1, 11.5, 10.9, 10.2, 9.8, 9.4, 9],
                        "relative_humidity_2m": [80, 83, 84, 84, 87, 91, 94, 97, 100, 100, 99, 88, 77, 71, 69, 68, 67, 66, 72, 77, 84, 87, 89, 91],
                        "precipitation": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.2, 0, 0.2, 0, 0, 0.2],
                        "wind_speed_10m": [0.8, 1.8, 2.1, 2.9, 2.3, 3.1, 3.6, 3.6, 3.6, 3.8, 3.6, 3.6, 4.6, 5.4, 5.4, 5, 4.3, 2.7, 3.8, 4, 3.6, 2.6, 2.8, 3.1]
                    }
                }
            },
        ]

        result = self.transformer.extract_hourly_records(test_data)

        assert len(result) == 24
        assert 'city_id' in result[0]
        assert 'weather_date' in result[0]
        assert 'weather_hour' in result[0]
        assert 'date_hour' in result[0]
        assert 'temperature' in result[0]
        assert 'humidity' in result[0]
        assert 'precipitation' in result[0]
        assert 'feels_like_temperature' in result[0]
        assert 'wind_speed' in result[0]
        assert 'temperature' in result[0]




