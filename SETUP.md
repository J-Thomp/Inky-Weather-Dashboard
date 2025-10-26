# Weather Dashboard Setup Guide

This guide will help you set up the Weather Dashboard on your Raspberry Pi to run automatically on boot and update every 30 minutes.

## Prerequisites

- Raspberry Pi with Inky Impression display connected
- SSH access to your Raspberry Pi
- Internet connection

## Initial Setup

### 1. Clone the Repository

```bash
cd ~
git clone https://github.com/YOUR_USERNAME/Inky-Weather-Dashboard.git
cd Inky-Weather-Dashboard
```

### 2. Install Dependencies

```bash
chmod +x install.sh
./install.sh
```

This will install:
- Python dependencies (requests, pillow, inky, schedule, python-dotenv)
- Required fonts
- Weather icons

### 3. Configure Your API Key

```bash
cp .env.example .env
nano .env
```

Edit the `.env` file with your settings:

```
OPENWEATHER_API_KEY=your_api_key_here
CITY_NAME=YourCity
COUNTRY_CODE=US
UNITS=imperial
```

Save and exit (Ctrl+X, then Y, then Enter)

### 4. Test the Setup

```bash
python3 weather_dashboard.py --test
```

This will run a single update to verify everything is working.

## Automatic Startup with Systemd

### 1. Copy the Service File

```bash
sudo cp weather-dashboard.service /etc/systemd/system/
```

### 2. Update the Service File (if needed)

If your username is not 'pi', edit the service file:

```bash
sudo nano /etc/systemd/system/weather-dashboard.service
```

Change `User=pi` to your username.

### 3. Enable and Start the Service

```bash
# Reload systemd to recognize the new service
sudo systemctl daemon-reload

# Enable the service to start on boot
sudo systemctl enable weather-dashboard.service

# Start the service now
sudo systemctl start weather-dashboard.service
```

### 4. Check Service Status

```bash
sudo systemctl status weather-dashboard.service
```

You should see "Active: active (running)" if everything is working correctly.

### 5. View Logs

```bash
# View real-time logs
sudo journalctl -u weather-dashboard.service -f

# View recent logs
sudo journalctl -u weather-dashboard.service -n 50
```

## Service Management Commands

```bash
# Start the service
sudo systemctl start weather-dashboard.service

# Stop the service
sudo systemctl stop weather-dashboard.service

# Restart the service
sudo systemctl restart weather-dashboard.service

# Disable auto-start on boot
sudo systemctl disable weather-dashboard.service

# Check service status
sudo systemctl status weather-dashboard.service
```

## Update Schedule

The dashboard will:
- ✓ Update weather data every **30 minutes** (configurable in config.py)
- ✓ Refresh automatically at **midnight (00:00)** to update day names
- ✓ Start automatically when the Raspberry Pi boots
- ✓ Restart automatically if the service crashes

## Troubleshooting

### Service won't start

1. Check the logs:
   ```bash
   sudo journalctl -u weather-dashboard.service -n 50
   ```

2. Verify Python path:
   ```bash
   which python3
   ```

3. Test manually:
   ```bash
   cd ~/Inky-Weather-Dashboard
   python3 weather_dashboard.py --test
   ```

### Display not updating

1. Check if service is running:
   ```bash
   sudo systemctl status weather-dashboard.service
   ```

2. Restart the service:
   ```bash
   sudo systemctl restart weather-dashboard.service
   ```

### API errors

1. Verify your API key is correct in `.env`
2. Check if you've exceeded OpenWeather API rate limits (60 calls/minute free tier)
3. Test API connection:
   ```bash
   python3 weather_api.py
   ```

## Updating the Code

When you pull new changes from the repository:

```bash
cd ~/Inky-Weather-Dashboard
git pull
sudo systemctl restart weather-dashboard.service
```

## Clean Up Test Files

The repository includes test files that you don't need on the Pi. They're already excluded in `.gitignore`:

- `test_*.py` - Test scripts
- `verify_*.py` - Diagnostic scripts
- `*.log` - Log files
- `weather_display.png` - Generated preview images

These won't be committed to git, but you can delete them manually if desired:

```bash
rm -f test_*.py verify_*.py *.log weather_display.png
```

## Configuration

Edit `config.py` to customize:

- `UPDATE_INTERVAL_MINUTES` - How often to update (default: 30)
- `CITY_NAME` - Your city
- `COUNTRY_CODE` - Your country code
- `UNITS` - Temperature units (imperial/metric)

After changes, restart the service:

```bash
sudo systemctl restart weather-dashboard.service
```
