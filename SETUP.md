## 24/7 Weather Collection - Setup Guide

## Overview

This is a **standalone weather collection system** that runs 24/7 on GitHub Actions (free) to collect weather data for horse racing. It keeps your trading system private while giving you continuous weather coverage.

### What Gets Published to GitHub

**Only these files (all safe to be public):**
- `weather_collector.py` - Collection script
- `weather.py` - Weather API interface
- `race_schedule.json` - Race schedule (just venue, date, time)
- `data/weather.db` - Weather database (collected data only)

**Your trading system stays private:**
- ✅ No betting data
- ✅ No database structure
- ✅ No trading strategies
- ✅ No local files

---

## Setup (15 minutes)

### Step 1: Create GitHub Repository (3 min)

1. Go to https://github.com/new
2. Repository name: `horse-racing-weather-cloud`
3. **Must be PUBLIC** (for free GitHub Actions)
4. Add README: Yes
5. Click "Create repository"

### Step 2: Upload This Folder (5 min)

**Option A - GitHub Desktop (Easiest):**
1. Download GitHub Desktop: https://desktop.github.com/
2. File → Add Local Repository
3. Choose: `C:\Users\henne\Desktop\horse-racing-weather-cloud`
4. Click "Publish repository"
5. Ensure "Keep private" is UNCHECKED
6. Click "Publish"

**Option B - Command Line:**
```bash
cd C:\Users\henne\Desktop\horse-racing-weather-cloud
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/horse-racing-weather-cloud.git
git push -u origin main
```

### Step 3: Enable GitHub Actions (1 min)

1. Go to your repository on GitHub
2. Click "Actions" tab
3. Click "I understand my workflows, enable them"

### Step 4: Configure Download Script (3 min)

On your LOCAL computer, edit:
`C:\Users\henne\Desktop\TradingAndValue\BetAngel\download_cloud_weather.py`

Change line 19:
```python
GITHUB_USER = 'YOUR_GITHUB_USERNAME'  # Put your actual username here
```

Example:
```python
GITHUB_USER = 'johndoe123'
```

### Step 5: Test It (3 min)

**From your local computer:**

```bash
# Export race schedule
cd C:\Users\henne\Desktop\TradingAndValue\BetAngel
python export_race_schedule.py

# Copy the generated race_schedule.json
copy race_schedule.json C:\Users\henne\Desktop\horse-racing-weather-cloud\

# Push to GitHub
cd C:\Users\henne\Desktop\horse-racing-weather-cloud
git add race_schedule.json
git commit -m "Add race schedule"
git push
```

**Trigger first cloud collection:**
1. Go to GitHub → Actions tab
2. Click "Weather Collection"
3. Click "Run workflow" → "Run workflow"
4. Wait 1-2 minutes
5. Should see green checkmark

**Download weather data:**
```bash
cd C:\Users\henne\Desktop\TradingAndValue\BetAngel
python download_cloud_weather.py
```

Should see: `[OK] Updated: X`

---

## Daily Workflow

### Morning - Before Racing (5 minutes)

```bash
# 1. Export today's race schedule
cd C:\Users\henne\Desktop\TradingAndValue\BetAngel
python export_race_schedule.py

# 2. Copy to cloud repository
copy race_schedule.json C:\Users\henne\Desktop\horse-racing-weather-cloud\

# 3. Push to GitHub
cd C:\Users\henne\Desktop\horse-racing-weather-cloud
git add race_schedule.json
git commit -m "Update schedule for [today's date]"
git push

# 4. Download overnight weather
cd C:\Users\henne\Desktop\TradingAndValue\BetAngel
python download_cloud_weather.py
```

**That's it!** Cloud collects weather automatically every 2 hours.

### Optional - Create Batch File

Create `morning_weather_routine.bat` on your desktop:

```batch
@echo off
cd C:\Users\henne\Desktop\TradingAndValue\BetAngel

echo Exporting race schedule...
python export_race_schedule.py

echo Copying to cloud repo...
copy race_schedule.json C:\Users\henne\Desktop\horse-racing-weather-cloud\

cd C:\Users\henne\Desktop\horse-racing-weather-cloud
echo Pushing to GitHub...
git add race_schedule.json
git commit -m "Update schedule"
git push

cd C:\Users\henne\Desktop\TradingAndValue\BetAngel
echo Downloading weather data...
python download_cloud_weather.py

echo.
echo Done! Press any key to close.
pause
```

Then just double-click this file each morning!

---

## How It Works

```
Your Computer (Private)          GitHub (Public)           Open-Meteo API
     │                                │                         │
     ├─ Export race schedule ─────────┤                         │
     │  (just venue/date/time)        │                         │
     │                                │                         │
     │                         [Every 2 hours]                  │
     │                                │                         │
     │                         weather_collector.py ────────────┤
     │                                │                         │
     │                                │              Weather data returned
     │                                │                         │
     │                         data/weather.db ◄────────────────┘
     │                                │
     │                         [Commit to repo]
     │                                │
     ├─ Download weather.db ──────────┤
     │                                │
     ├─ Import to local database      │
     │                                │
     ▼                                ▼
  Ready to trade!            Keeps collecting 24/7!
```

---

## Privacy & Security

### What's Safe to Upload

✅ **weather_collector.py** - Generic collection script
✅ **weather.py** - API interface (no credentials)
✅ **race_schedule.json** - Just public race info (venue, date, time)
✅ **data/weather.db** - Only weather data, no betting/trading data

### What Stays Private (On Your Computer)

🔒 **enhanced_race_data.db** - Your main trading database
🔒 **Race results & outcomes** - All betting data
🔒 **TPD/telemetry data** - Live race data
🔒 **Trading strategies** - Your system logic
🔒 **Guardian configuration** - Bet Angel setup

### GitHub Repository Contents

Your public repository will contain:
- Weather collection scripts (generic, reusable)
- Race schedule (public information anyway)
- Collected weather data (public information)
- No trading system, no betting data, no proprietary code

---

## Verification

### Check Cloud is Working

```bash
# Method 1: GitHub website
Go to: https://github.com/YOUR_USERNAME/horse-racing-weather-cloud/actions
Look for: Green checkmarks every 2 hours

# Method 2: Check commits
Go to: https://github.com/YOUR_USERNAME/horse-racing-weather-cloud/commits
Look for: "Update weather data - YYYY-MM-DD HH:MM UTC"
```

### Check Local Database

```bash
cd C:\Users\henne\Desktop\TradingAndValue\BetAngel
python -c "import sqlite3; conn=sqlite3.connect('data/enhanced_race_data.db'); c=conn.cursor(); c.execute('SELECT COUNT(*) FROM pre_race_conditions WHERE weather_fetched_at IS NOT NULL'); print(f'Races with weather: {c.fetchone()[0]}'); conn.close()"
```

### Check Cloud Database

Download and inspect:
1. Go to: https://github.com/YOUR_USERNAME/horse-racing-weather-cloud
2. Navigate to: data/weather.db
3. Click "Download"
4. Open with SQLite browser

---

## Troubleshooting

### "Actions not running"

**Check:** Repository is public
- Settings → Danger Zone → Change visibility → Public

**Check:** Actions are enabled
- Actions tab → Enable workflows

### "Can't download weather.db"

**Check:** Collection has run at least once
- Actions tab → Should see successful run

**Check:** Username is correct in download script
- Edit download_cloud_weather.py
- Verify GITHUB_USER matches your username

### "No races in schedule"

**Solution:** Export races again
```bash
cd C:\Users\henne\Desktop\TradingAndValue\BetAngel
python export_race_schedule.py
```

---

## Cost

| Service | Free Tier | Our Usage | Cost |
|---------|-----------|-----------|------|
| GitHub Actions | 2,000 min/month | ~1,800 min | $0.00 |
| Open-Meteo API | 10,000 calls/day | ~96 calls/day | $0.00 |
| Storage | 500 MB | <10 MB | $0.00 |
| **Total** | - | - | **$0.00/month** |

---

## FAQ

**Q: Is it safe to make this repository public?**
A: Yes! It only contains weather collection code and weather data. Your trading system stays completely private on your computer.

**Q: Can someone steal my data?**
A: The repository only contains:
- Weather data (publicly available anyway)
- Race schedule (public information)
- Generic collection scripts (no proprietary logic)

Your trading database, betting data, and strategies never leave your computer.

**Q: What if someone copies my repository?**
A: That's fine! The code is generic weather collection. They'd need their own race schedule and can't access your trading system.

**Q: How do I delete everything if needed?**
A: Just delete the GitHub repository. Your local trading system is completely unaffected.

**Q: Do I need to keep horse-racing-weather-cloud folder?**
A: Yes, you need it to update race_schedule.json and push to GitHub. But it's separate from your trading system.

---

## Files Overview

**On GitHub (Public):**
```
horse-racing-weather-cloud/
├── README.md                    # Public description
├── SETUP.md                     # This file
├── weather_collector.py         # Collection script
├── weather.py                   # Weather API
├── race_schedule.json           # Race schedule (updated daily)
├── .github/workflows/collect.yml  # Automation
└── data/
    └── weather.db               # Weather database
```

**On Your Computer (Private):**
```
TradingAndValue/BetAngel/
├── data/
│   └── enhanced_race_data.db   # Your trading database (NEVER uploaded)
├── export_race_schedule.py     # Export schedule
└── download_cloud_weather.py   # Download weather
```

---

## Summary

You now have:

✅ 24/7 weather collection (GitHub Actions)
✅ Complete privacy (trading system stays local)
✅ Simple daily workflow (5 minutes)
✅ Zero cost ($0/month)
✅ Full weather history

Your trading system is completely separate and private. Only the generic weather collection system is public.

Happy racing! 🏇
