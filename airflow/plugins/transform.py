from datetime import datetime
from typing import List, Dict, Optional
import logging

class WeatherTransform:

    def __init__(self, wind_speed: float = 5.0):
        self.wind_speed = wind_speed

        self.logger = logging.getLogger(__name__)

        self.temp_thresholds= {
            'extreme_cold' : -10,
            'cold' : 0,
            'cool' : 10,
            'warm' : 20,
            'hot' : 30,
            'extreme_hot' : 40 
        }
    

    def extract_hourly_records(self, raw_data: List[Dict]):
        hourly_records = []

        for city_data in raw_data:
            city_id = city_data.get('city_id')
            city_name = city_data.get('city_name')
            raw_json = city_data.get('raw_json', {})

            if not raw_json or 'hourly' not in raw_json:
                self.logger.warning(f"Not enough data for {city_name}")
                continue

            hourly_data = raw_json['hourly']

            num_records = len(hourly_data['time'])

            for i in range (num_records):
                record = {
                    'city_id' : city_id,
                    'city_name' : city_name,
                }

                date = self.safe_get(hourly_data, 'time', i)
                date_array = date.split('T')

                record['weather_hour'] = int( date_array[1].split(':')[0])
                
                record['weather_date'] = date_array[0]
                record['date_hour'] = date 

                record['temperature'] = self.safe_get(hourly_data, 'temperature_2m', i)
                record['humidity'] = self.safe_get(hourly_data, 'relative_humidity_2m', i)
                record['precipitation'] = self.safe_get(hourly_data, 'precipitation', i)
                record['wind_speed'] = self.safe_get(hourly_data, 'wind_speed_10m', i)
                record['feels_like_temperature'] = self.calculate_feels_like(record['temperature'], record['humidity'], record['wind_speed'])

                hourly_records.append(record)
                    
                self.logger.info(f"Extracted {num_records} for {city_name}")

        return hourly_records


    def safe_get(self, data_dict: Dict, key: str, index: int, default=None):
        try:
            if key in data_dict and index < len(data_dict[key]):
                return data_dict[key][index] if data_dict[key][index] is not None else default
            return default
        except (IndexError, TypeError, KeyError):
            return default

    def transform(self, raw_data: List[Dict]):
        try:
            return self.extract_hourly_records(raw_data)
        
        except Exception as e:
            self.logger.error(f"Error during transformation: {str(e)}")

    def calculate_feels_like(self, temp, humidity, wind_speed):
        if temp <= 10 and wind_speed > 4.8:
            return (13.12+(0.615*float(temp))-(11.37*(float(wind_speed)*3.6)**0.16)+(0.3965*float(temp))*((float(wind_speed)*3.6)**0.16))
        elif temp >= 27:
            return round((-8.78469475556 + (1.61139411 * temp) + (2.33854883889 * humidity) + (-0.14611605 * temp * humidity) + (-0.012308094 * (temp**2)) + (-0.0164248277778 * (humidity**2)) + (0.002211732 * (temp**2) * humidity) + (0.00072546 * temp * (humidity**2)) + (-0.000003582 * (temp**2) * (humidity**2))) * 5/9 + 32, 2)
        else:
            return temp

    