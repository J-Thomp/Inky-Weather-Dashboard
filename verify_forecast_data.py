#!/usr/bin/env python3
"""
Diagnostic script to verify OpenWeather API forecast data
Shows the raw API response and how it's being processed
"""
from weather_api import WeatherAPI
from datetime import datetime
import json

def verify_forecast_data():
    """Fetch and display forecast data with detailed breakdown"""
    try:
        print("="*80)
        print("OPENWEATHER API FORECAST DATA VERIFICATION")
        print("="*80)
        print()

        # Initialize API
        weather = WeatherAPI()
        print(f"Fetching forecast data for: {weather.city}, {weather.country}")
        print()

        # Get the processed weather data
        data = weather.get_weather_data()

        if not data or not data.get('forecast'):
            print("ERROR: No forecast data received!")
            return

        forecast = data['forecast']
        daily = forecast.get('daily', [])

        print(f"Total daily forecast entries received: {len(daily)}")
        print()
        print("="*80)
        print("DAILY FORECAST DATA (as processed by weather_api.py)")
        print("="*80)
        print()

        for i, day in enumerate(daily[:10]):  # Show up to 10 days
            print(f"Day {i}: {day['date']} ({day['day_name']})")
            print(f"  Min Temp: {day['min_temp']}°F")
            print(f"  Max Temp: {day['max_temp']}°F")
            print(f"  Description: {day['description']}")
            print(f"  Icon: {day['icon']}")
            print(f"  Humidity: {day['humidity']}%")
            print(f"  Wind Speed: {day['wind_speed']} mph")
            print()

        print("="*80)
        print("DISPLAY LOGIC VERIFICATION")
        print("="*80)
        print()

        # Apply the same logic as weather_display_pil.py
        daily_forecasts = daily[0:6]  # First 6 days including today

        print(f"Cards to be displayed: {len(daily_forecasts)}")
        print()

        for i, day in enumerate(daily_forecasts):
            # Override day name for first card to show "Today"
            day_name = 'Today' if i == 0 else day['day_name']

            print(f"Card {i+1} ({day_name:8}): {day['date']} | {day['min_temp']}/{day['max_temp']}°F | {day['description']}")

        print()
        print("="*80)
        print("VERIFICATION CHECKLIST")
        print("="*80)
        print()

        # Get today's date for verification
        today = datetime.now().date()

        if len(daily) > 0:
            first_day = daily[0]['date']
            print(f"✓ Today's date: {today}")
            print(f"✓ First forecast entry date: {first_day}")

            if first_day == today:
                print("✓ PASS: First entry is today's date")
            else:
                print("✗ FAIL: First entry is NOT today's date!")
                print(f"  Expected: {today}")
                print(f"  Got: {first_day}")
                print(f"  Difference: {(first_day - today).days} day(s)")

            print()
            print("Expected card order:")
            for i in range(min(6, len(daily))):
                expected_date = datetime.now().date()
                from datetime import timedelta
                expected_date = expected_date + timedelta(days=i)
                actual_date = daily[i]['date']
                day_name = 'Today' if i == 0 else daily[i]['day_name']

                match = "✓" if expected_date == actual_date else "✗"
                print(f"  {match} Card {i+1} ({day_name}): Expected {expected_date} | Got {actual_date}")

        print()
        print("="*80)

    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    verify_forecast_data()
