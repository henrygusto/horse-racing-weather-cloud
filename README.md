# Horse Racing Weather Collection (Cloud)

24/7 weather data collection for horse racing using GitHub Actions.

## What This Does

Collects comprehensive weather data every 2 hours for upcoming horse races, running in the cloud even when your computer is off.

## Features

- ✅ Runs 24/7 on GitHub Actions (free)
- ✅ Collects weather from Open-Meteo API
- ✅ Stores data in SQLite database
- ✅ Download to your local system when needed
- ✅ 100% free (uses free tier limits)

## Setup

See [SETUP.md](SETUP.md) for complete instructions.

## Quick Start

1. Fork/clone this repository
2. Edit `race_schedule.json` with your races
3. Push to GitHub
4. Enable GitHub Actions
5. Weather collection starts automatically!

## Files

- `weather_collector.py` - Main collection script
- `weather.py` - Weather API interface
- `race_schedule.json` - Races to collect weather for (update daily)
- `.github/workflows/collect.yml` - GitHub Actions automation
- `data/weather.db` - Weather database (created automatically)

## Daily Workflow

1. Update `race_schedule.json` with today's races
2. Commit and push to GitHub
3. Download `weather.db` from GitHub when you need it
4. Import into your local database

## Cost

**$0.00/month** - Uses free tiers of GitHub Actions and Open-Meteo API

## Data Collected

- Temperature, humidity, wind, precipitation
- Soil moisture (3 depths)
- Rainfall history (1h, 3h, 6h, 24h, 7d)
- Ground saturation, predicted going
- Track drying/wetting indicators

50+ weather variables per race.
