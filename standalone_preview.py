#!/usr/bin/env python3
"""
Standalone preview of the weather dashboard
No dependencies needed except PIL (Pillow)
Run: python standalone_preview.py
"""

from PIL import Image, ImageDraw, ImageFont
from datetime import datetime, timedelta

class WeatherDisplayPreview:
    def __init__(self):
        self.width = 800
        self.height = 480

        # Colors for Inky Spectra (7-color e-ink) - RGB values
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.YELLOW = (255, 255, 0)
        self.BLUE = (0, 0, 255)
        self.GREEN = (0, 255, 0)
        self.ORANGE = (255, 140, 0)

        # Layout constants
        self.PADDING = 20
        self.HEADER_HEIGHT = 60
        self.MAIN_SECTION_HEIGHT = 240
        self.FORECAST_HEIGHT = self.height - self.HEADER_HEIGHT - self.MAIN_SECTION_HEIGHT - self.PADDING * 2

        # Try to load fonts
        try:
            self.font_xl = ImageFont.truetype("arial.ttf", 72)
            self.font_large = ImageFont.truetype("arial.ttf", 36)
            self.font_title = ImageFont.truetype("arial.ttf", 24)
            self.font_medium = ImageFont.truetype("arial.ttf", 18)
            self.font_small = ImageFont.truetype("arial.ttf", 14)
            self.font_tiny = ImageFont.truetype("arial.ttf", 11)
        except:
            print("Using default fonts (Arial not found)")
            self.font_xl = ImageFont.load_default()
            self.font_large = ImageFont.load_default()
            self.font_title = ImageFont.load_default()
            self.font_medium = ImageFont.load_default()
            self.font_small = ImageFont.load_default()
            self.font_tiny = ImageFont.load_default()

    def get_weather_icon_text(self, icon_code):
        """Map OpenWeatherMap icon codes to emoji/symbols"""
        icon_map = {
            '01d': '☀',  '01n': '🌙',
            '02d': '⛅', '02n': '☁',
            '03d': '☁',  '03n': '☁',
            '04d': '☁',  '04n': '☁',
            '09d': '🌧', '09n': '🌧',
            '10d': '🌦', '10n': '🌧',
            '11d': '⛈',  '11n': '⛈',
            '13d': '❄',  '13n': '❄',
            '50d': '🌫', '50n': '🌫',
        }
        return icon_map.get(icon_code, '🌤')

    def get_wind_arrow(self, degrees):
        """Convert wind direction to arrow"""
        degrees = degrees % 360
        arrows = ['↓', '↙', '←', '↖', '↑', '↗', '→', '↘']
        index = round(degrees / 45) % 8
        return arrows[index]

    def get_icon_color(self, icon_code):
        """Get color for weather icon based on condition"""
        if icon_code.startswith('01'):  # Clear
            return self.YELLOW  # Sunny
        elif icon_code.startswith(('02', '03', '04')):  # Clouds
            return self.WHITE  # Cloudy
        elif icon_code.startswith(('09', '10')):  # Rain
            return self.BLUE  # Rain
        elif icon_code.startswith('11'):  # Thunderstorm
            return self.RED  # Storm
        elif icon_code.startswith('13'):  # Snow
            return self.WHITE  # Snow
        else:  # Mist etc
            return self.WHITE  # Mist

    def get_temp_color(self, temp):
        """Get color for temperature based on value"""
        if temp >= 80:
            return self.RED  # Hot
        elif temp >= 70:
            return self.ORANGE  # Warm
        elif temp >= 60:
            return self.YELLOW  # Mild
        elif temp >= 50:
            return self.GREEN  # Cool
        else:
            return self.BLUE  # Cold

    def draw_header(self, draw, weather_data):
        """Draw the header with location and date"""
        if not weather_data:
            return

        # Draw colored header background
        draw.rectangle([0, 0, self.width, self.HEADER_HEIGHT],
                      fill=(200, 220, 255), outline=self.BLUE, width=3)

        # Location
        location = f"{weather_data['city']}, {weather_data['country']}"
        draw.text((self.PADDING, self.PADDING), location,
                 font=self.font_title, fill=self.BLACK)

        # Date with color
        date_text = weather_data['timestamp'].strftime('%A, %B %d')
        draw.text((self.PADDING, self.PADDING + 32), date_text,
                 font=self.font_small, fill=self.BLUE)

    def draw_circular_icon(self, draw, x, y, radius, icon_code):
        """Draw a circular weather icon"""
        # Draw circle background
        circle_color = self.get_icon_color(icon_code)
        draw.ellipse([x - radius, y - radius, x + radius, y + radius],
                    fill=circle_color, outline=self.BLACK, width=2)

        # Draw icon text in center
        icon_text = self.get_weather_icon_text(icon_code)
        text_bbox = draw.textbbox((0, 0), icon_text, font=self.font_xl)
        text_w = text_bbox[2] - text_bbox[0]
        text_h = text_bbox[3] - text_bbox[1]
        draw.text((x - text_w // 2, y - text_h // 2 - 10), icon_text,
                 font=self.font_xl, fill=self.BLACK)

    def draw_main_weather(self, draw, weather_data):
        """Draw the main weather section with icon and details"""
        if not weather_data:
            return

        y_start = self.HEADER_HEIGHT + self.PADDING

        # Draw subtle background for main section
        draw.rectangle([0, self.HEADER_HEIGHT, self.width,
                       self.HEADER_HEIGHT + self.MAIN_SECTION_HEIGHT],
                      fill=(245, 250, 255))

        # Draw large circular icon on the left
        icon_x = 120
        icon_y = y_start + 90
        icon_radius = 70
        self.draw_circular_icon(draw, icon_x, icon_y, icon_radius, weather_data['icon'])

        # Main temperature with color
        temp_text = f"{weather_data['temperature']}°"
        temp_x = 220
        temp_y = y_start + 40
        temp_color = self.get_temp_color(weather_data['temperature'])
        draw.text((temp_x, temp_y), temp_text, font=self.font_xl, fill=temp_color)

        # Feels like
        feels_text = f"Feels like {weather_data['feels_like']}°"
        draw.text((temp_x, temp_y + 85), feels_text, font=self.font_small, fill=self.BLACK)

        # Right side: Two columns of details
        col1_x = 420
        col2_x = 620
        detail_y = y_start + 10
        line_height = 35

        # Column 1
        details_col1 = [
            ('Sunrise', weather_data['sunrise'].strftime('%I:%M %p'), self.ORANGE),
            ('Sunset', weather_data['sunset'].strftime('%I:%M %p'), self.BLUE),
            (f'High', f"{weather_data.get('temp_max', '--')}°", self.RED),
            (f'Low', f"{weather_data.get('temp_min', '--')}°", self.BLUE),
            ('Humidity', f"{weather_data['humidity']}%", self.BLUE),
            ('Pressure', f"{weather_data['pressure']} hPa", self.BLACK),
        ]

        for i, (label, value, color) in enumerate(details_col1):
            y = detail_y + i * line_height
            draw.text((col1_x, y), label, font=self.font_tiny, fill=self.BLACK)
            draw.text((col1_x, y + 15), value, font=self.font_small, fill=color)

        # Column 2
        wind_arrow = self.get_wind_arrow(weather_data['wind_direction'])
        details_col2 = [
            (f'{wind_arrow} Wind', f"{weather_data['wind_speed']} mph", self.BLUE),
            ('UV Index', f"{weather_data.get('uv_index', 'N/A')}", self.ORANGE),
            ('Visibility', f"{weather_data.get('visibility', 10):.1f} mi", self.BLACK),
            ('Air Quality', weather_data.get('air_quality', {}).get('description', 'N/A'), self.GREEN),
        ]

        for i, (label, value, color) in enumerate(details_col2):
            y = detail_y + i * line_height
            draw.text((col2_x, y), label, font=self.font_tiny, fill=self.BLACK)
            draw.text((col2_x, y + 15), value, font=self.font_small, fill=color)

    def draw_temperature_timeline(self, draw, hourly_data, x, y, width, height):
        """Draw temperature timeline graph"""
        if not hourly_data or len(hourly_data) < 2:
            return

        # Extract temperatures
        temps = [h['temp'] for h in hourly_data]
        times = [h['time'] for h in hourly_data]

        min_temp = min(temps)
        max_temp = max(temps)
        temp_range = max_temp - min_temp if max_temp != min_temp else 1

        # Draw graph background
        graph_height = 40
        graph_y = y + 5

        # Calculate points
        points = []
        step = width / (len(temps) - 1) if len(temps) > 1 else width

        for i, temp in enumerate(temps):
            px = x + i * step
            py = graph_y + graph_height - ((temp - min_temp) / temp_range) * graph_height
            points.append((px, py))

        # Draw line with gradient effect
        if len(points) > 1:
            for i in range(len(points) - 1):
                temp_color = self.get_temp_color(temps[i])
                draw.line([points[i], points[i+1]], fill=temp_color, width=3)

        # Draw points with temperature-based colors
        for i, point in enumerate(points):
            temp_color = self.get_temp_color(temps[i])
            draw.ellipse([point[0]-4, point[1]-4, point[0]+4, point[1]+4],
                        fill=temp_color, outline=self.BLACK, width=1)

        # Draw time labels under the graph
        label_y = graph_y + graph_height + 8
        for i, time in enumerate(times):
            if i % 2 == 0:
                px = x + i * step
                time_text = time.strftime('%I%p').lstrip('0')
                draw.text((px - 15, label_y), time_text, font=self.font_tiny, fill=self.BLACK)

    def draw_forecast(self, draw, forecast_data):
        """Draw 7-day forecast cards"""
        if not forecast_data:
            return

        section_y = self.HEADER_HEIGHT + self.MAIN_SECTION_HEIGHT + self.PADDING

        # Draw timeline first
        timeline_height = 70
        self.draw_temperature_timeline(draw, forecast_data.get('hourly', []),
                                      self.PADDING + 10, section_y,
                                      self.width - self.PADDING * 2 - 20,
                                      timeline_height)

        # Draw forecast cards
        cards_y = section_y + timeline_height + 10
        daily_forecasts = forecast_data.get('daily', [])[:7]

        if not daily_forecasts:
            return

        card_width = (self.width - self.PADDING * 2) / len(daily_forecasts)
        card_height = 100

        for i, day in enumerate(daily_forecasts):
            card_x = self.PADDING + i * card_width
            self.draw_forecast_card(draw, day, card_x, cards_y, card_width, card_height)

    def draw_forecast_card(self, draw, day_data, x, y, width, height):
        """Draw a single forecast card"""
        # Get background color based on weather
        bg_color = self.get_icon_color(day_data['icon'])

        # Draw card background with color
        draw.rectangle([x + 2, y, x + width - 2, y + height],
                      fill=bg_color, outline=self.BLACK, width=2)

        # Day name
        day_name = day_data['day_name']
        text_bbox = draw.textbbox((0, 0), day_name, font=self.font_small)
        text_w = text_bbox[2] - text_bbox[0]
        draw.text((x + width // 2 - text_w // 2, y + 8), day_name,
                 font=self.font_small, fill=self.BLACK)

        # Weather icon (smaller)
        icon = self.get_weather_icon_text(day_data['icon'])
        icon_bbox = draw.textbbox((0, 0), icon, font=self.font_medium)
        icon_w = icon_bbox[2] - icon_bbox[0]
        draw.text((x + width // 2 - icon_w // 2, y + 32), icon,
                 font=self.font_medium, fill=self.BLACK)

        # Temperature range with colors
        high_color = self.get_temp_color(day_data['max_temp'])
        low_color = self.get_temp_color(day_data['min_temp'])

        # Draw high temp
        high_text = f"{day_data['max_temp']}°"
        high_bbox = draw.textbbox((0, 0), high_text, font=self.font_small)
        high_w = high_bbox[2] - high_bbox[0]
        draw.text((x + width // 2 - high_w - 3, y + 70), high_text,
                 font=self.font_small, fill=high_color)

        # Draw separator
        draw.text((x + width // 2 - 3, y + 70), "/",
                 font=self.font_small, fill=self.BLACK)

        # Draw low temp
        low_text = f"{day_data['min_temp']}°"
        draw.text((x + width // 2 + 5, y + 70), low_text,
                 font=self.font_small, fill=low_color)

    def create_preview(self, weather_data):
        """Create preview image"""
        img = Image.new("RGB", (self.width, self.height), (255, 255, 255))
        draw = ImageDraw.Draw(img)

        # Draw all sections
        self.draw_header(draw, weather_data['current'])
        self.draw_main_weather(draw, weather_data['current'])
        self.draw_forecast(draw, weather_data.get('forecast'))

        # Draw last updated in bottom right
        last_updated = weather_data.get('last_updated', datetime.now())
        timestamp_text = f"Updated: {last_updated.strftime('%I:%M %p')}"
        text_bbox = draw.textbbox((0, 0), timestamp_text, font=self.font_tiny)
        text_w = text_bbox[2] - text_bbox[0]
        draw.text((self.width - text_w - self.PADDING, self.height - 20),
                 timestamp_text, font=self.font_tiny, fill=self.BLACK)

        return img


def main():
    print("🌤️  Generating Weather Dashboard Preview...")
    print("=" * 50)

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
                {'time': datetime.now().replace(hour=20, minute=0), 'temp': 54, 'icon': '02d'},
                {'time': datetime.now().replace(hour=2, minute=0) + timedelta(days=1), 'temp': 55, 'icon': '02d'},
                {'time': datetime.now().replace(hour=8, minute=0) + timedelta(days=1), 'temp': 53, 'icon': '02d'},
                {'time': datetime.now().replace(hour=14, minute=0) + timedelta(days=1), 'temp': 57, 'icon': '01d'},
                {'time': datetime.now().replace(hour=20, minute=0) + timedelta(days=1), 'temp': 60, 'icon': '01d'},
                {'time': datetime.now().replace(hour=2, minute=0) + timedelta(days=2), 'temp': 58, 'icon': '02d'},
            ],
            'daily': [
                {
                    'date': datetime.now().date(),
                    'day_name': 'Today',
                    'min_temp': 54,
                    'max_temp': 53,
                    'description': 'Partly Cloudy',
                    'icon': '02d',
                },
                {
                    'date': datetime.now().date() + timedelta(days=1),
                    'day_name': 'Tomorrow',
                    'min_temp': 58,
                    'max_temp': 46,
                    'description': 'Partly Cloudy',
                    'icon': '02d',
                },
                {
                    'date': datetime.now().date() + timedelta(days=2),
                    'day_name': 'Sat',
                    'min_temp': 57,
                    'max_temp': 43,
                    'description': 'Partly Cloudy',
                    'icon': '02d',
                },
                {
                    'date': datetime.now().date() + timedelta(days=3),
                    'day_name': 'Sun',
                    'min_temp': 54,
                    'max_temp': 45,
                    'description': 'Partly Cloudy',
                    'icon': '02d',
                },
                {
                    'date': datetime.now().date() + timedelta(days=4),
                    'day_name': 'Mon',
                    'min_temp': 56,
                    'max_temp': 46,
                    'description': 'Partly Cloudy',
                    'icon': '02d',
                },
                {
                    'date': datetime.now().date() + timedelta(days=5),
                    'day_name': 'Tue',
                    'min_temp': 55,
                    'max_temp': 47,
                    'description': 'Partly Cloudy',
                    'icon': '02d',
                },
            ]
        },
        'last_updated': datetime.now()
    }

    # Create preview
    display = WeatherDisplayPreview()
    img = display.create_preview(sample_data)

    # Save the image
    output_file = 'weather_preview.png'
    img.save(output_file)

    print("\n✅ Preview generated successfully!")
    print(f"📄 Saved to: {output_file}")
    print("\nOpen the file to see what your dashboard will look like!")
    print("\nTo test different conditions, edit the sample_data in this file:")
    print("  • Change 'icon' codes: 01d=sunny, 02d=partly cloudy, 10d=rainy, 13d=snow")
    print("  • Adjust temperatures to see different colors")
    print("  • Modify any weather values")

if __name__ == "__main__":
    main()
