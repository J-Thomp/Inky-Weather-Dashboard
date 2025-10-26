#!/bin/bash
# Cleanup script to remove test and temporary files

echo "Cleaning up test and temporary files..."

# Remove test scripts
rm -f test_*.py
rm -f verify_*.py

# Remove old preview/test files
rm -f html_to_image.py
rm -f html_weather_preview.py
rm -f preview_display.py
rm -f standalone_preview.py
rm -f update_display.py
rm -f weather_display_html.py

# Remove HTML/CSS test files
rm -f weather.html
rm -f weather.css
rm -f weather_rendered.html

# Remove generated images
rm -f Current.jpg
rm -f weather_display.png

# Remove log files
rm -f *.log

# Remove old display file (if using PIL version)
rm -f weather_display.py

# Remove old env example
rm -f env_example.txt

# Remove Python cache
rm -rf __pycache__

echo "Cleanup complete!"
echo ""
echo "Files kept:"
echo "  - weather_dashboard.py (main application)"
echo "  - weather_api.py (API handler)"
echo "  - weather_display_pil.py (display renderer)"
echo "  - config.py (configuration)"
echo "  - weather-dashboard.service (systemd service)"
echo "  - install.sh (installation script)"
echo "  - download_icons.py (icon downloader)"
echo "  - .env (your API keys - NOT tracked in git)"
echo "  - .env.example (template)"
echo "  - icons/ (weather icons)"
echo "  - inspiration.png (design reference)"
echo ""
