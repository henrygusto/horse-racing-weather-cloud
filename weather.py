#!/usr/bin/env python3
"""
Weather data collection using Open-Meteo API

This is a standalone copy of the weather module for cloud deployment.
Does not require any other project dependencies.
"""

import requests
from datetime import datetime, timedelta
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)

# Racecourse/Racetrack Coordinates (UK & USA)
VENUE_COORDS = {
    # UK Racecourses
    "Newbury": {"lat": 51.4008, "lon": -1.3267, "country": "UK", "tz": "Europe/London"},
    "Cheltenham": {"lat": 51.9117, "lon": -2.0493, "country": "UK", "tz": "Europe/London"},
    "Ascot": {"lat": 51.4088, "lon": -0.6764, "country": "UK", "tz": "Europe/London"},
    "Kempton Park": {"lat": 51.4175, "lon": -0.3867, "country": "UK", "tz": "Europe/London"},
    "Lingfield": {"lat": 51.1817, "lon": -0.0100, "country": "UK", "tz": "Europe/London"},
    "Worcester": {"lat": 52.1886, "lon": -2.2274, "country": "UK", "tz": "Europe/London"},
    "Aintree": {"lat": 53.4775, "lon": -2.9497, "country": "UK", "tz": "Europe/London"},
    "York": {"lat": 53.9536, "lon": -1.0353, "country": "UK", "tz": "Europe/London"},
    "Sandown": {"lat": 51.3867, "lon": -0.3644, "country": "UK", "tz": "Europe/London"},
    "Haydock": {"lat": 53.4750, "lon": -2.6503, "country": "UK", "tz": "Europe/London"},
    "Doncaster": {"lat": 53.5229, "lon": -1.0958, "country": "UK", "tz": "Europe/London"},
    "Newmarket": {"lat": 52.2438, "lon": 0.3611, "country": "UK", "tz": "Europe/London"},
    "Goodwood": {"lat": 50.8692, "lon": -0.7464, "country": "UK", "tz": "Europe/London"},
    "Epsom": {"lat": 51.3178, "lon": -0.2617, "country": "UK", "tz": "Europe/London"},
    "Ayr": {"lat": 55.4583, "lon": -4.6333, "country": "UK", "tz": "Europe/London"},
    "Newcastle": {"lat": 54.9783, "lon": -1.6178, "country": "UK", "tz": "Europe/London"},
    "Chepstow": {"lat": 51.6431, "lon": -2.6764, "country": "UK", "tz": "Europe/London"},
    "Fontwell": {"lat": 50.8667, "lon": -0.6167, "country": "UK", "tz": "Europe/London"},
    "Ludlow": {"lat": 52.3667, "lon": -2.7333, "country": "UK", "tz": "Europe/London"},
    "Market Rasen": {"lat": 53.4333, "lon": -0.3333, "country": "UK", "tz": "Europe/London"},
    "Sedgefield": {"lat": 54.6667, "lon": -1.4667, "country": "UK", "tz": "Europe/London"},
    "Southwell": {"lat": 53.0833, "lon": -0.9500, "country": "UK", "tz": "Europe/London"},
    "Uttoxeter": {"lat": 52.9000, "lon": -1.8667, "country": "UK", "tz": "Europe/London"},
    "Wetherby": {"lat": 53.9333, "lon": -1.3833, "country": "UK", "tz": "Europe/London"},
    "Wolverhampton": {"lat": 52.5833, "lon": -2.1333, "country": "UK", "tz": "Europe/London"},
    "Bangor-on-Dee": {"lat": 52.9910, "lon": -2.9235, "country": "UK", "tz": "Europe/London"},
    "Bath": {"lat": 51.4183, "lon": -2.4094, "country": "UK", "tz": "Europe/London"},
    "Brighton": {"lat": 50.8248, "lon": -0.1072, "country": "UK", "tz": "Europe/London"},
    "Chester": {"lat": 53.1852, "lon": -2.8932, "country": "UK", "tz": "Europe/London"},
    "Ffos Las": {"lat": 51.7311, "lon": -4.2400, "country": "UK", "tz": "Europe/London"},
    "Hexham": {"lat": 54.9522, "lon": -2.1245, "country": "UK", "tz": "Europe/London"},
    "Newton Abbot": {"lat": 50.5365, "lon": -3.5920, "country": "UK", "tz": "Europe/London"},
    "Plumpton": {"lat": 50.9216, "lon": -0.0570, "country": "UK", "tz": "Europe/London"},
    "Ripon": {"lat": 54.1207, "lon": -1.4923, "country": "UK", "tz": "Europe/London"},
    "Yarmouth": {"lat": 52.6263, "lon": 1.7338, "country": "UK", "tz": "Europe/London"},

    # USA Racetracks
    "Churchill Downs": {"lat": 38.2048, "lon": -85.7702, "country": "USA", "tz": "America/New_York"},
    "Keeneland": {"lat": 38.0403, "lon": -84.5909, "country": "USA", "tz": "America/New_York"},
    "Santa Anita": {"lat": 34.1395, "lon": -118.0377, "country": "USA", "tz": "America/Los_Angeles"},
    "Del Mar": {"lat": 32.9789, "lon": -117.2651, "country": "USA", "tz": "America/Los_Angeles"},
    "Gulfstream Park": {"lat": 25.9898, "lon": -80.1373, "country": "USA", "tz": "America/New_York"},
    "Belmont Park": {"lat": 40.7155, "lon": -73.7201, "country": "USA", "tz": "America/New_York"},
    "Saratoga": {"lat": 43.0687, "lon": -73.7896, "country": "USA", "tz": "America/New_York"},
    "Pimlico": {"lat": 39.3419, "lon": -76.6653, "country": "USA", "tz": "America/New_York"},
}


def get_comprehensive_weather(venue: str, race_datetime: datetime) -> Optional[Dict]:
    """
    Get comprehensive weather data using Open-Meteo API.

    Args:
        venue: Racecourse name (e.g., "Newbury", "Churchill Downs")
        race_datetime: datetime object of race start time

    Returns:
        Dictionary with comprehensive weather data, or None if error
    """
    coords = VENUE_COORDS.get(venue)
    if not coords:
        logger.warning(f"No coordinates for venue: {venue}")
        return None

    country = coords.get('country', 'UK')

    # Date range: 7 days before race for historical context
    end_date = race_datetime.date()
    start_date = end_date - timedelta(days=7)

    url = "https://api.open-meteo.com/v1/forecast"

    # Auto-detect units based on country
    if country == 'USA':
        temp_unit = 'fahrenheit'
        wind_unit = 'mph'
        precip_unit = 'inch'
    else:
        temp_unit = 'celsius'
        wind_unit = 'ms'
        precip_unit = 'mm'

    params = {
        'latitude': coords['lat'],
        'longitude': coords['lon'],

        'hourly': ','.join([
            'temperature_2m',
            'apparent_temperature',
            'precipitation',
            'rain',
            'wind_speed_10m',
            'wind_direction_10m',
            'wind_gusts_10m',
            'relative_humidity_2m',
            'dew_point_2m',
            'soil_moisture_0_to_1cm',
            'soil_moisture_1_to_3cm',
            'soil_moisture_3_to_9cm',
            'soil_temperature_0cm',
            'soil_temperature_6cm',
            'et0_fao_evapotranspiration',
            'pressure_msl',
            'cloud_cover',
            'visibility',
            'weather_code',
            'precipitation_probability'
        ]),

        'temperature_unit': temp_unit,
        'wind_speed_unit': wind_unit,
        'precipitation_unit': precip_unit,
        'timezone': coords.get('tz', 'Europe/London'),
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d')
    }

    try:
        logger.info(f"Fetching weather for {venue} at {race_datetime.isoformat()}")
        response = requests.get(url, params=params, timeout=10)

        if response.status_code != 200:
            logger.error(f"HTTP {response.status_code}")
            return None

        data = response.json()
        hourly = data.get('hourly', {})
        times = hourly.get('time', [])

        # Find race time
        race_time_str = race_datetime.strftime('%Y-%m-%dT%H:00')

        if race_time_str in times:
            idx = times.index(race_time_str)

            # Calculate historical accumulations
            rainfall_1h = hourly['precipitation'][idx] if idx > 0 else 0
            rainfall_3h = sum(hourly['precipitation'][max(0,idx-3):idx]) if idx >= 3 else 0
            rainfall_6h = sum(hourly['precipitation'][max(0,idx-6):idx]) if idx >= 6 else 0
            rainfall_24h = sum(hourly['precipitation'][max(0,idx-24):idx]) if idx >= 24 else 0
            rainfall_7d = sum(hourly['precipitation'][:idx]) if idx > 0 else 0

            # Calculate hours since last rain
            hours_since_rain = 0
            for i in range(idx-1, -1, -1):
                if hourly['precipitation'][i] > 0.1:
                    break
                hours_since_rain += 1

            # Calculate ground saturation index
            ground_saturation = (
                hourly['soil_moisture_0_to_1cm'][idx] * 0.5 +
                hourly['soil_moisture_1_to_3cm'][idx] * 0.3 +
                hourly['soil_moisture_3_to_9cm'][idx] * 0.2
            )

            # Net moisture (rain - evaporation)
            et_24h = hourly['et0_fao_evapotranspiration'][idx] * 24
            net_moisture_24h = rainfall_24h - et_24h

            # Predict going from soil moisture
            soil_moisture_surface = hourly['soil_moisture_0_to_1cm'][idx]
            if soil_moisture_surface < 0.15:
                predicted_going = "Firm"
            elif soil_moisture_surface < 0.25:
                predicted_going = "Good"
            elif soil_moisture_surface < 0.35:
                predicted_going = "Soft"
            else:
                predicted_going = "Heavy"

            # Track condition trend
            if idx >= 3:
                moisture_3h_ago = hourly['soil_moisture_0_to_1cm'][idx-3]
                track_drying = soil_moisture_surface < moisture_3h_ago
                track_wetting = soil_moisture_surface > moisture_3h_ago
            else:
                track_drying = False
                track_wetting = False

            result = {
                'venue': venue,
                'country': country,
                'race_datetime': race_datetime.isoformat(),

                # Basic conditions
                'temperature': hourly['temperature_2m'][idx],
                'apparent_temperature': hourly['apparent_temperature'][idx],
                'precipitation_current': hourly['precipitation'][idx],
                'rain_current': hourly['rain'][idx],
                'wind_speed': hourly['wind_speed_10m'][idx],
                'wind_direction': hourly['wind_direction_10m'][idx],
                'wind_gusts': hourly['wind_gusts_10m'][idx],
                'humidity': hourly['relative_humidity_2m'][idx],
                'dew_point': hourly['dew_point_2m'][idx],
                'pressure': hourly['pressure_msl'][idx],
                'cloud_cover': hourly['cloud_cover'][idx],
                'visibility': hourly['visibility'][idx],
                'weather_code': hourly['weather_code'][idx],
                'precipitation_probability': hourly['precipitation_probability'][idx],

                # Ground conditions
                'soil_moisture_0_1cm': hourly['soil_moisture_0_to_1cm'][idx],
                'soil_moisture_1_3cm': hourly['soil_moisture_1_to_3cm'][idx],
                'soil_moisture_3_9cm': hourly['soil_moisture_3_to_9cm'][idx],
                'soil_temperature_0cm': hourly['soil_temperature_0cm'][idx],
                'soil_temperature_6cm': hourly['soil_temperature_6cm'][idx],
                'evapotranspiration': hourly['et0_fao_evapotranspiration'][idx],

                # Historical accumulations
                'rainfall_1h': rainfall_1h,
                'rainfall_3h': rainfall_3h,
                'rainfall_6h': rainfall_6h,
                'rainfall_24h': rainfall_24h,
                'rainfall_7d': rainfall_7d,

                # Derived features
                'ground_saturation_index': ground_saturation,
                'net_moisture_24h': net_moisture_24h,
                'hours_since_rain': hours_since_rain,
                'predicted_going': predicted_going,
                'track_drying': track_drying,
                'track_wetting': track_wetting,

                # Units & metadata
                'temp_unit': '°F' if country == 'USA' else '°C',
                'wind_unit': 'mph' if country == 'USA' else 'm/s',
                'precip_unit': 'in' if country == 'USA' else 'mm',
                'data_quality': 'comprehensive',
                'fetched_at': datetime.now().isoformat()
            }

            logger.info(f"[OK] Weather data retrieved for {venue}")
            return result

        else:
            logger.error(f"Race time {race_time_str} not in response")
            return None

    except Exception as e:
        logger.error(f"Error fetching weather: {e}")
        return None
