# Constanta Water Temperature

Simple Windows application that displays current water temperature in the Black Sea near Constanta, Romania.

## Features

- 🌊 Shows current water temperature
- ⏰ Auto-refresh every hour
- 🔄 Manual refresh button
- 🌙 Dark theme interface
- ⚠️ Shows last known data on network error
- 📅 Last update timestamp

## Installation and Usage

### Option 1: Pre-built EXE
1. Download `water_temp.exe` from releases
2. Run with double click

### Option 2: From source
1. Install Python 3.7+
2. Install dependencies:
```bash
pip install requests beautifulsoup4
```
3. Run:
```bash
python water_temp.py
```

## Building EXE

```bash
pip install pyinstaller
pyinstaller --onefile --windowed water_temp.py
```

## Data Source

The app fetches data from: https://ro.seatemperature.net/current/romania/constanta

## Screenshot

![App Screenshot](screenshot.png)

## Requirements

- Windows 10/11
- Internet connection

## License

MIT License
