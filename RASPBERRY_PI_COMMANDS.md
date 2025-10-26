# Quick Setup Commands for Raspberry Pi

## One-Time Setup (Run these commands via SSH)

```bash
# 1. Navigate to your project directory
cd ~/Inky-Weather-Dashboard

# 2. Pull the latest changes
git pull

# 3. Make sure .env file exists with your API key
# (if you haven't done this already)
cp .env.example .env
nano .env
# Edit the file, save with Ctrl+X, Y, Enter

# 4. Run the automated setup script
chmod +x start_service.sh
./start_service.sh
```

That's it! The service is now running and will:
- ✓ Start automatically on boot
- ✓ Update weather every 30 minutes
- ✓ Refresh at midnight to update day names
- ✓ Restart automatically if it crashes

## Optional: Clean Up Test Files

```bash
# Remove test files from your local directory
chmod +x cleanup.sh
./cleanup.sh
```

## Useful Commands

### Check Service Status
```bash
sudo systemctl status weather-dashboard.service
```

### View Live Logs
```bash
sudo journalctl -u weather-dashboard.service -f
```

Press Ctrl+C to stop viewing logs.

### Restart Service (after making code changes)
```bash
sudo systemctl restart weather-dashboard.service
```

### Stop Service
```bash
sudo systemctl stop weather-dashboard.service
```

### Start Service
```bash
sudo systemctl start weather-dashboard.service
```

### Disable Auto-Start on Boot
```bash
sudo systemctl disable weather-dashboard.service
```

### Re-Enable Auto-Start
```bash
sudo systemctl enable weather-dashboard.service
```

## Updating the Code

When you push new changes from your computer:

```bash
# On Raspberry Pi via SSH
cd ~/Inky-Weather-Dashboard
git pull
sudo systemctl restart weather-dashboard.service
```

## Troubleshooting

### Check if service is running
```bash
sudo systemctl status weather-dashboard.service
```

### View last 50 log entries
```bash
sudo journalctl -u weather-dashboard.service -n 50
```

### Test manually (without service)
```bash
cd ~/Inky-Weather-Dashboard
python3 weather_dashboard.py --test
```

This runs a single update to test if everything works.

## What's Configured

- **Update Interval:** Every 30 minutes (configurable in `config.py`)
- **Midnight Refresh:** Automatic refresh at 00:00 daily
- **Auto-Start:** Enabled on boot
- **Auto-Restart:** Service restarts if it crashes
- **Working Directory:** `~/Inky-Weather-Dashboard`
