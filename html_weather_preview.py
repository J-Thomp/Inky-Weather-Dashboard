#!/usr/bin/env python3
"""
HTML-based Weather Dashboard Preview
Uses Jinja2 templates and html2image for rendering
"""

from datetime import datetime, timedelta
from jinja2 import Template
import os

def generate_html_preview():
    """Generate weather dashboard using HTML template"""

    print("Generating HTML-based weather dashboard...")

    # Hourly data for the graph (temperature and rain)
    hourly_data = [
        {'time': '10 AM', 'temp': 50, 'rain_chance': 10},
        {'time': '12 PM', 'temp': 52, 'rain_chance': 5},
        {'time': '2 PM', 'temp': 54, 'rain_chance': 0},
        {'time': '4 PM', 'temp': 56, 'rain_chance': 0},
        {'time': '6 PM', 'temp': 54, 'rain_chance': 15},
        {'time': '8 PM', 'temp': 51, 'rain_chance': 20},
        {'time': '10 PM', 'temp': 49, 'rain_chance': 25},
        {'time': '12 AM', 'temp': 48, 'rain_chance': 30},
        {'time': '2 AM', 'temp': 47, 'rain_chance': 35},
        {'time': '4 AM', 'temp': 46, 'rain_chance': 20},
        {'time': '6 AM', 'temp': 48, 'rain_chance': 10},
    ]

    # Calculate min and max temps for scaling
    temps = [h['temp'] for h in hourly_data]
    temp_min = min(temps)
    temp_max = max(temps)

    # Sample weather data
    weather_data = {
        'city': 'Conshohocken',
        'country': 'PA',
        'current_date': datetime.now().strftime('%A, %B %d'),
        'temperature': 54,
        'feels_like': 51,
        'temp_high': 56,
        'temp_low': 51,
        'current_icon': '02d',
        'humidity': 60,
        'wind_speed': 5.99,
        'pressure': 1016,
        'sunrise': '7:20 AM',
        'sunset': '6:10 PM',
        'visibility': '>10.0',
        'uv_index': 2.9,
        'air_quality': '2 /10',
        'hourly_data': hourly_data,
        'temp_min': temp_min,
        'temp_max': temp_max,
        'forecast': [
            {'day_name': 'Fri', 'icon': '02d', 'max_temp': 50, 'min_temp': 46},
            {'day_name': 'Sat', 'icon': '02d', 'max_temp': 54, 'min_temp': 47},
            {'day_name': 'Sun', 'icon': '02d', 'max_temp': 68, 'min_temp': 53},
            {'day_name': 'Mon', 'icon': '01d', 'max_temp': 62, 'min_temp': 68},
            {'day_name': 'Tue', 'icon': '01d', 'max_temp': 89, 'min_temp': 52},
            {'day_name': 'Wed', 'icon': '01d', 'max_temp': 74, 'min_temp': 57},
            {'day_name': 'Thu', 'icon': '02d', 'max_temp': 73, 'min_temp': 58},
        ],
        'last_updated': datetime.now().strftime('%I:%M%p').lstrip('0')
    }

    # Read HTML template
    with open('weather.html', 'r', encoding='utf-8') as f:
        template_content = f.read()

    # Render template with Jinja2
    template = Template(template_content)
    html_output = template.render(**weather_data)

    # Save rendered HTML
    output_html = 'weather_rendered.html'
    with open(output_html, 'w', encoding='utf-8') as f:
        f.write(html_output)

    print(f"[OK] Rendered HTML saved to: {output_html}")
    print("\nTo convert to image:")
    print("1. Install html2image: pip install html2image")
    print("2. Run: python html_to_image.py")
    print("\nOr open weather_rendered.html in your browser to preview!")

if __name__ == "__main__":
    generate_html_preview()
