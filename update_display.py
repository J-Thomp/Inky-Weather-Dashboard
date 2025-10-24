#!/usr/bin/env python3
"""
Simple script to update Inky display with weather using HTML template
This version creates the HTML and you can view it in a browser
For automatic image generation, you'll need to install html2image
"""

from weather_api import WeatherAPI
from weather_display_html import WeatherDisplay
import sys

def main():
    print("=" * 50)
    print("Weather Dashboard Update")
    print("=" * 50)

    try:
        # Fetch weather data
        print("\nFetching weather data...")
        weather_api = WeatherAPI()
        weather_data = weather_api.get_weather_data()

        if not weather_data or not weather_data.get('current'):
            print("❌ Failed to fetch weather data")
            sys.exit(1)

        print(f"✅ Weather data fetched for {weather_data['current']['city']}")
        print(f"   Temperature: {weather_data['current']['temperature']}°F")

        # Update display
        print("\nUpdating display...")
        display = WeatherDisplay()
        display.update_display(weather_data)

        print("\n" + "=" * 50)
        print("✅ Update complete!")
        print("=" * 50)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
