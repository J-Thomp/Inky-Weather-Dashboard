#!/usr/bin/env python3
"""
Preview the weather dashboard display without Inky hardware
This creates a PNG file that you can view on your computer
"""

import sys
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime, timedelta

class MockInkyDisplay:
    """Mock display object that simulates Inky Impression"""
    def __init__(self):
        self.width = 800
        self.height = 480
        self.resolution = f"{self.width}x{self.height}"

    def set_image(self, img):
        self.image = img

    def show(self):
        # Don't actually show on hardware, just save
        pass

def mock_auto():
    """Replace the auto() function to return mock display"""
    return MockInkyDisplay()

# Create a mock inky module before importing weather_display
from types import SimpleNamespace

# Create mock modules
inky_auto_module = SimpleNamespace(auto=mock_auto)
inky_module = SimpleNamespace(auto=inky_auto_module)

# Add mock to sys.modules before importing weather_display
sys.modules['inky'] = inky_module
sys.modules['inky.auto'] = inky_auto_module

# Now we can import weather_display
from weather_display import WeatherDisplay

def generate_preview():
    """Generate a preview of the weather display"""
    print("Generating weather dashboard preview...")

    # Create display instance
    display = WeatherDisplay()

    # Create sample weather data
    sample_data = {
        'current': {
            'city': 'Conshohocken',
            'country': 'US',
            'temperature': 54,
            'feels_like': 51,
            'temp_min': 51,
            'temp_max': 56,
            'description': 'Partly Cloudy',
            'icon': '02d',
            'humidity': 60,
            'wind_speed': 5.99,
            'wind_direction': 180,
            'pressure': 1016,
            'sunrise': datetime.now().replace(hour=7, minute=20),
            'sunset': datetime.now().replace(hour=18, minute=10),
            'visibility': 10.0,
            'uv_index': 2.9,
            'air_quality': {'index': 1, 'description': 'Fair'},
            'timestamp': datetime.now()
        },
        'forecast': {
            'hourly': [
                {'time': datetime.now().replace(hour=8, minute=0), 'temp': 54, 'icon': '02d'},
                {'time': datetime.now().replace(hour=14, minute=0), 'temp': 55, 'icon': '02d'},
                {'time': datetime.now().replace(hour=20, minute=0), 'temp': 53, 'icon': '02d'},
                {'time': datetime.now() + timedelta(hours=8), 'temp': 57, 'icon': '01d'},
                {'time': datetime.now() + timedelta(hours=14), 'temp': 60, 'icon': '01d'},
                {'time': datetime.now() + timedelta(hours=20), 'temp': 58, 'icon': '02d'},
            ],
            'daily': [
                {
                    'date': datetime.now().date(),
                    'day_name': 'Today',
                    'min_temp': 54,
                    'max_temp': 53,
                    'description': 'Partly Cloudy',
                    'icon': '02d',
                    'humidity': 60,
                    'wind_speed': 5.99
                },
                {
                    'date': datetime.now().date() + timedelta(days=1),
                    'day_name': 'Tomorrow',
                    'min_temp': 58,
                    'max_temp': 46,
                    'description': 'Partly Cloudy',
                    'icon': '02d',
                    'humidity': 55,
                    'wind_speed': 4.5
                },
                {
                    'date': datetime.now().date() + timedelta(days=2),
                    'day_name': 'Sat',
                    'min_temp': 57,
                    'max_temp': 43,
                    'description': 'Partly Cloudy',
                    'icon': '02d',
                    'humidity': 50,
                    'wind_speed': 3.8
                },
                {
                    'date': datetime.now().date() + timedelta(days=3),
                    'day_name': 'Sun',
                    'min_temp': 54,
                    'max_temp': 45,
                    'description': 'Partly Cloudy',
                    'icon': '02d',
                    'humidity': 52,
                    'wind_speed': 4.2
                },
                {
                    'date': datetime.now().date() + timedelta(days=4),
                    'day_name': 'Mon',
                    'min_temp': 56,
                    'max_temp': 46,
                    'description': 'Partly Cloudy',
                    'icon': '02d',
                    'humidity': 58,
                    'wind_speed': 5.1
                },
                {
                    'date': datetime.now().date() + timedelta(days=5),
                    'day_name': 'Tue',
                    'min_temp': 55,
                    'max_temp': 47,
                    'description': 'Partly Cloudy',
                    'icon': '02d',
                    'humidity': 60,
                    'wind_speed': 5.5
                }
            ]
        },
        'last_updated': datetime.now()
    }

    # Update the display with sample data
    display.update_display(sample_data)

    print("\n✅ Preview generated successfully!")
    print("📄 Check 'weather_display.png' to see what your display will look like")
    print("\nTo test with different weather conditions, you can:")
    print("  1. Edit the sample_data in this file")
    print("  2. Change icon codes (01d=sunny, 02d=partly cloudy, 10d=rainy, etc.)")
    print("  3. Adjust temperatures to see different colors")

if __name__ == "__main__":
    generate_preview()
