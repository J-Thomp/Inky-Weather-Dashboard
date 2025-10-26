#!/usr/bin/env python3
"""
Test script to verify forecast display logic
"""
from datetime import datetime, timedelta

# Simulate forecast data
forecast_data = []
for i in range(10):
    date = datetime.now().date() + timedelta(days=i)
    day_name = date.strftime('%a')
    forecast_data.append({
        'date': date,
        'day_name': day_name,
        'min_temp': 45 + i,
        'max_temp': 55 + i,
        'description': 'Partly Cloudy',
        'icon': '02d'
    })

print("Full forecast data (10 days):")
for i, day in enumerate(forecast_data):
    print(f"  Day {i}: {day['date']} - {day['day_name']} - {day['min_temp']}/{day['max_temp']}°F - Icon: {day['icon']}")

print("\n" + "="*60)
print("Display logic: Show 6 cards starting with Today")
print("="*60 + "\n")

# Apply the display logic (same as in weather_display_pil.py)
daily_forecasts = forecast_data[0:6]  # Get first 6 days including today

print(f"Cards to display: {len(daily_forecasts)}\n")

for i, day in enumerate(daily_forecasts):
    # Override day name for first card to show "Today"
    day_display = day.copy()
    if i == 0:
        day_display['day_name'] = 'Today'

    print(f"Card {i+1}: {day_display['day_name']:8} | Date: {day['date']} | Temps: {day['min_temp']}/{day['max_temp']}°F | Icon: {day['icon']}")

print("\nExpected output:")
print("  Card 1: Today")
print("  Card 2: Tomorrow's day (e.g., Sun)")
print("  Card 3-6: Next 4 days (e.g., Mon, Tue, Wed, Thu)")
