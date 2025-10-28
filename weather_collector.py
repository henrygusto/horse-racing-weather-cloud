#!/usr/bin/env python3
"""
Cloud Weather Collector - Standalone version

Runs in GitHub Actions to collect weather data 24/7.
This version is completely independent - no other project files needed.

Author: Claude Code
Date: October 2025
"""

import os
import sys
import sqlite3
import json
from datetime import datetime, timedelta
from pathlib import Path

# Import weather module (in same directory)
from weather import get_comprehensive_weather, VENUE_COORDS


class WeatherCollector:
    """Standalone weather collector for GitHub Actions"""

    def __init__(self, db_path='data/weather.db', config_path='race_schedule.json'):
        self.db_path = db_path
        self.config_path = config_path
        self.ensure_database()

    def ensure_database(self):
        """Create database and table if they don't exist"""
        os.makedirs(os.path.dirname(self.db_path) if os.path.dirname(self.db_path) else '.', exist_ok=True)

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS weather_updates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                market_id TEXT NOT NULL,
                venue TEXT NOT NULL,
                race_date TEXT NOT NULL,
                race_time TEXT NOT NULL,

                -- Core weather
                temperature REAL,
                apparent_temperature REAL,
                precipitation_current REAL,
                rain_current REAL,
                wind_speed REAL,
                wind_direction REAL,
                wind_gusts REAL,
                humidity REAL,
                dew_point REAL,
                pressure REAL,
                cloud_cover REAL,
                visibility REAL,
                weather_code INTEGER,
                precipitation_probability REAL,

                -- Ground conditions
                soil_moisture_0_1cm REAL,
                soil_moisture_1_3cm REAL,
                soil_moisture_3_9cm REAL,
                soil_temperature_0cm REAL,
                soil_temperature_6cm REAL,
                evapotranspiration REAL,

                -- Historical rainfall
                rainfall_1h REAL,
                rainfall_3h REAL,
                rainfall_6h REAL,
                rainfall_24h REAL,
                rainfall_7d REAL,

                -- Derived features
                ground_saturation_index REAL,
                net_moisture_24h REAL,
                hours_since_rain INTEGER,
                predicted_going TEXT,
                track_drying INTEGER,
                track_wetting INTEGER,

                -- Metadata
                weather_data_quality TEXT,
                weather_fetched_at TEXT NOT NULL,
                temperature_unit TEXT,
                wind_speed_unit TEXT,
                collection_timestamp TEXT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_weather_market_time
            ON weather_updates(market_id, collection_timestamp)
        """)

        conn.commit()
        conn.close()

        print(f"[OK] Database ready: {self.db_path}")

    def load_race_schedule(self):
        """Load race schedule from JSON config file"""
        if not os.path.exists(self.config_path):
            print(f"WARNING: Race schedule not found: {self.config_path}")
            print("Using demo schedule for testing")
            return self.get_demo_schedule()

        with open(self.config_path, 'r') as f:
            schedule = json.load(f)

        print(f"[OK] Loaded {len(schedule)} races from schedule")
        return schedule

    def get_demo_schedule(self):
        """Demo schedule for testing"""
        tomorrow = datetime.now() + timedelta(days=1)

        demo_races = [
            {
                'market_id': 'demo.001',
                'venue': 'Newbury',
                'race_date': tomorrow.strftime('%Y-%m-%d'),
                'race_time': '14:30'
            },
            {
                'market_id': 'demo.002',
                'venue': 'Kempton Park',
                'race_date': tomorrow.strftime('%Y-%m-%d'),
                'race_time': '15:00'
            }
        ]

        print(f"[INFO] Using demo schedule with {len(demo_races)} races")
        return demo_races

    def collect_weather_for_race(self, race):
        """Collect weather for a single race"""
        market_id = race['market_id']
        venue = race['venue']
        race_date = race['race_date']
        race_time = race['race_time']

        race_datetime = datetime.fromisoformat(f"{race_date}T{race_time}:00")

        print(f"\n[RACE] {venue} | {race_date} | {race_time}")
        print(f"   Market ID: {market_id}")

        if venue not in VENUE_COORDS:
            print(f"   [WARN] SKIP: No coordinates for venue '{venue}'")
            return None

        weather = get_comprehensive_weather(venue, race_datetime)

        if not weather:
            print(f"   [ERROR] Failed to fetch weather")
            return None

        print(f"   [OK] Weather fetched")
        print(f"   Temp: {weather.get('temperature', 'N/A')}{weather.get('temp_unit', '')}")
        print(f"   Wind: {weather.get('wind_speed', 'N/A')} {weather.get('wind_unit', '')}")
        print(f"   Going: {weather.get('predicted_going', 'N/A')}")

        return {
            'market_id': market_id,
            'venue': venue,
            'race_date': race_date,
            'race_time': race_time,
            'weather': weather
        }

    def save_weather_update(self, race_data):
        """Save weather update to database"""
        if not race_data or not race_data.get('weather'):
            return False

        market_id = race_data['market_id']
        venue = race_data['venue']
        race_date = race_data['race_date']
        race_time = race_data['race_time']
        weather = race_data['weather']

        collection_time = datetime.now().isoformat()

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO weather_updates (
                    market_id, venue, race_date, race_time,
                    temperature, apparent_temperature, precipitation_current, rain_current,
                    wind_speed, wind_direction, wind_gusts, humidity, dew_point,
                    pressure, cloud_cover, visibility, weather_code, precipitation_probability,
                    soil_moisture_0_1cm, soil_moisture_1_3cm, soil_moisture_3_9cm,
                    soil_temperature_0cm, soil_temperature_6cm, evapotranspiration,
                    rainfall_1h, rainfall_3h, rainfall_6h, rainfall_24h, rainfall_7d,
                    ground_saturation_index, net_moisture_24h, hours_since_rain,
                    predicted_going, track_drying, track_wetting,
                    weather_data_quality, weather_fetched_at, temperature_unit, wind_speed_unit,
                    collection_timestamp
                ) VALUES (
                    ?, ?, ?, ?,
                    ?, ?, ?, ?,
                    ?, ?, ?, ?, ?,
                    ?, ?, ?, ?, ?,
                    ?, ?, ?,
                    ?, ?, ?,
                    ?, ?, ?, ?, ?,
                    ?, ?, ?,
                    ?, ?, ?,
                    ?, ?, ?, ?,
                    ?
                )
            """, (
                market_id, venue, race_date, race_time,
                weather.get('temperature'), weather.get('apparent_temperature'),
                weather.get('precipitation_current'), weather.get('rain_current'),
                weather.get('wind_speed'), weather.get('wind_direction'),
                weather.get('wind_gusts'), weather.get('humidity'),
                weather.get('dew_point'), weather.get('pressure'),
                weather.get('cloud_cover'), weather.get('visibility'),
                weather.get('weather_code'), weather.get('precipitation_probability'),
                weather.get('soil_moisture_0_1cm'), weather.get('soil_moisture_1_3cm'),
                weather.get('soil_moisture_3_9cm'), weather.get('soil_temperature_0cm'),
                weather.get('soil_temperature_6cm'), weather.get('evapotranspiration'),
                weather.get('rainfall_1h'), weather.get('rainfall_3h'),
                weather.get('rainfall_6h'), weather.get('rainfall_24h'),
                weather.get('rainfall_7d'), weather.get('ground_saturation_index'),
                weather.get('net_moisture_24h'), weather.get('hours_since_rain'),
                weather.get('predicted_going'), weather.get('track_drying'),
                weather.get('track_wetting'), weather.get('data_quality'),
                weather.get('fetched_at'), weather.get('temp_unit'),
                weather.get('wind_unit'), collection_time
            ))

            conn.commit()
            return True

        except Exception as e:
            print(f"   [ERROR] Database error: {e}")
            conn.rollback()
            return False

        finally:
            conn.close()

    def run_collection(self):
        """Main collection loop"""
        print("=" * 80)
        print(" CLOUD WEATHER COLLECTOR")
        print("=" * 80)
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()

        # Load schedule
        races = self.load_race_schedule()

        if not races:
            print("\n[WARN] No races to collect weather for")
            return

        # Filter to upcoming races only (within next 48 hours)
        now = datetime.now()
        cutoff = now + timedelta(hours=48)
        upcoming_races = []

        for race in races:
            race_dt = datetime.fromisoformat(f"{race['race_date']}T{race['race_time']}:00")
            if now <= race_dt <= cutoff:
                upcoming_races.append(race)

        print(f"Found {len(upcoming_races)} upcoming races (within 48 hours)")
        print()

        if not upcoming_races:
            print("[OK] No races need weather updates at this time")
            return

        # Collect weather for each race
        success_count = 0
        fail_count = 0

        for i, race in enumerate(upcoming_races, 1):
            print(f"\n[{i}/{len(upcoming_races)}]", end=' ')

            race_data = self.collect_weather_for_race(race)

            if race_data and self.save_weather_update(race_data):
                success_count += 1
            else:
                fail_count += 1

        # Summary
        print("\n" + "=" * 80)
        print(" COLLECTION SUMMARY")
        print("=" * 80)
        print(f"[OK] Successful: {success_count}")
        print(f"[ERROR] Failed: {fail_count}")
        print(f"Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()


def main():
    """Entry point"""
    collector = WeatherCollector()
    collector.run_collection()


if __name__ == '__main__':
    main()
