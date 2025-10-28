# Quick Start - 15 Minutes to 24/7 Weather Collection

## What You're Setting Up

A separate, standalone weather collection system that:
- Runs 24/7 on GitHub (free)
- Keeps your trading system completely private
- Downloads weather data to your local database

## 5-Step Setup

### 1. Create GitHub Repository (3 min)

**Go to:** https://github.com/new

**Settings:**
- Name: `horse-racing-weather-cloud`
- **Public** ← Must be public for free Actions
- Add README: Yes
- Click "Create repository"

### 2. Upload This Folder (5 min)

**Download GitHub Desktop:** https://desktop.github.com/

**Then:**
1. Install and sign in
2. File → Add Local Repository
3. Choose: `C:\Users\henne\Desktop\horse-racing-weather-cloud`
4. Click "Publish repository"
5. **Uncheck** "Keep this code private"
6. Click "Publish repository"

### 3. Enable GitHub Actions (1 min)

1. Go to your repository on GitHub
2. Click "Actions" tab
3. Click "I understand my workflows, enable them"

### 4. Configure Download Script (2 min)

**Edit:** `C:\Users\henne\Desktop\TradingAndValue\BetAngel\download_cloud_weather.py`

**Line 19 - Change:**
```python
GITHUB_USER = 'YOUR_GITHUB_USERNAME'
```

**To (your actual username):**
```python
GITHUB_USER = 'johndoe123'  # Your GitHub username
```

**Save the file.**

### 5. First Test (4 min)

**Open Command Prompt:**

```bash
# Export race schedule
cd C:\Users\henne\Desktop\TradingAndValue\BetAngel
python export_race_schedule.py

# Copy to cloud repo
copy race_schedule.json C:\Users\henne\Desktop\horse-racing-weather-cloud\

# Push to GitHub
cd C:\Users\henne\Desktop\horse-racing-weather-cloud
git add race_schedule.json
git commit -m "Initial schedule"
git push
```

**Trigger collection on GitHub:**
1. Go to your repository → Actions tab
2. Click "Weather Collection"
3. Click "Run workflow" → "Run workflow"
4. Wait 1-2 minutes → Green checkmark

**Download weather:**
```bash
cd C:\Users\henne\Desktop\TradingAndValue\BetAngel
python download_cloud_weather.py
```

Should see: `[OK] Updated: X`

---

## Done! 🎉

Your cloud weather collector is now running 24/7.

## Daily Routine (5 minutes)

Every morning:

```bash
# Export schedule
cd C:\Users\henne\Desktop\TradingAndValue\BetAngel
python export_race_schedule.py

# Copy to cloud
copy race_schedule.json C:\Users\henne\Desktop\horse-racing-weather-cloud\

# Push
cd C:\Users\henne\Desktop\horse-racing-weather-cloud
git add race_schedule.json
git commit -m "Update schedule"
git push

# Download overnight weather
cd C:\Users\henne\Desktop\TradingAndValue\BetAngel
python download_cloud_weather.py
```

**That's it!** Cloud collects every 2 hours automatically.

---

## Privacy

✅ **Your trading system stays private** - Never uploaded to GitHub
✅ **Only weather collection is public** - Generic, reusable code
✅ **No betting data** - Just race schedule (venue, date, time)

---

## Troubleshooting

**"Actions not running"**
- Repository must be public (Settings → Change visibility)

**"Can't download weather"**
- Check GitHub username in download script is correct
- Make sure cloud has run at least once (Actions tab)

**"No races in schedule"**
- Run export_race_schedule.py again
- Make sure enhanced_race_data.db has upcoming races

---

## Full Documentation

See `SETUP.md` for complete instructions and troubleshooting.

---

Happy racing! 🏇🌦️
