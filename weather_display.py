from PIL import Image, ImageDraw, ImageFont
from inky.auto import auto
from datetime import datetime
from config import *
import math

class WeatherDisplay:
    def __init__(self):
        try:
            self.display = auto()
            print(f"Detected display: {self.display.resolution}")
        except Exception as e:
            print(f"Error initializing display: {e}")
            print("Make sure your Inky Impression is properly connected")
            raise

        # Display dimensions
        self.width = self.display.width
        self.height = self.display.height

        # Colors for Inky Spectra (7-color e-ink) - RGB values
        # The display will convert these to its palette
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
            self.font_xl = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 72)
            self.font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36)
            self.font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
            self.font_medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
            self.font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
            self.font_tiny = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 11)
        except:
            print("Warning: Using default fonts")
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
        # Normalize degrees to 0-360
        degrees = degrees % 360
        arrows = ['↓', '↙', '←', '↖', '↑', '↗', '→', '↘']
        index = round(degrees / 45) % 8
        return arrows[index]

    def draw_header(self, draw, weather_data):
        """Draw the header with location and date"""
        if not weather_data:
            return

        # Location
        location = f"{weather_data['city']}, {weather_data['country']}"
        draw.text((self.PADDING, self.PADDING), location,
                 font=self.font_title, fill=self.BLACK)

        # Date
        date_text = weather_data['timestamp'].strftime('%A, %B %d')
        draw.text((self.PADDING, self.PADDING + 32), date_text,
                 font=self.font_small, fill=self.BLACK)

    def draw_circular_icon(self, draw, x, y, radius, icon_code):
        """Draw a circular weather icon"""
        # Draw circle background
        circle_color = self.get_icon_color(icon_code)
        draw.ellipse([x - radius, y - radius, x + radius, y + radius],
                    fill=circle_color, outline=self.BLACK, width=2)

        # Draw icon text in center
        icon_text = self.get_weather_icon_text(icon_code)
        # Center the emoji - approximate centering
        text_bbox = draw.textbbox((0, 0), icon_text, font=self.font_xl)
        text_w = text_bbox[2] - text_bbox[0]
        text_h = text_bbox[3] - text_bbox[1]
        draw.text((x - text_w // 2, y - text_h // 2 - 10), icon_text,
                 font=self.font_xl, fill=self.BLACK)

    def get_icon_color(self, icon_code):
        """Get color for weather icon based on condition"""
        # Using Inky Spectra's 7-color palette
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

    def draw_main_weather(self, draw, weather_data):
        """Draw the main weather section with icon and details"""
        if not weather_data:
            return

        y_start = self.HEADER_HEIGHT + self.PADDING

        # Draw large circular icon on the left
        icon_x = 120
        icon_y = y_start + 90
        icon_radius = 70
        self.draw_circular_icon(draw, icon_x, icon_y, icon_radius, weather_data['icon'])

        # Main temperature
        temp_text = f"{weather_data['temperature']}°"
        temp_x = 220
        temp_y = y_start + 40
        draw.text((temp_x, temp_y), temp_text, font=self.font_xl, fill=self.BLACK)

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
            ('Sunrise', weather_data['sunrise'].strftime('%I:%M %p')),
            ('Sunset', weather_data['sunset'].strftime('%I:%M %p')),
            (f'High', f"{weather_data.get('temp_max', '--')}°"),
            (f'Low', f"{weather_data.get('temp_min', '--')}°"),
            ('Humidity', f"{weather_data['humidity']}%"),
            ('Pressure', f"{weather_data['pressure']} hPa"),
        ]

        for i, (label, value) in enumerate(details_col1):
            y = detail_y + i * line_height
            draw.text((col1_x, y), label, font=self.font_tiny, fill=self.BLACK)
            draw.text((col1_x, y + 15), value, font=self.font_small, fill=self.BLACK)

        # Column 2
        wind_arrow = self.get_wind_arrow(weather_data['wind_direction'])
        details_col2 = [
            (f'{wind_arrow} Wind', f"{weather_data['wind_speed']} mph"),
            ('UV Index', f"{weather_data.get('uv_index', 'N/A')}"),
            ('Visibility', f"{weather_data.get('visibility', 10):.1f} mi"),
            ('Air Quality', weather_data.get('air_quality', {}).get('description', 'N/A')),
        ]

        for i, (label, value) in enumerate(details_col2):
            y = detail_y + i * line_height
            draw.text((col2_x, y), label, font=self.font_tiny, fill=self.BLACK)
            draw.text((col2_x, y + 15), value, font=self.font_small, fill=self.BLACK)

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
            # Invert y because higher temps should be higher on screen
            py = graph_y + graph_height - ((temp - min_temp) / temp_range) * graph_height
            points.append((px, py))

        # Draw line
        if len(points) > 1:
            draw.line(points, fill=self.BLACK, width=2)

        # Draw points
        for point in points:
            draw.ellipse([point[0]-3, point[1]-3, point[0]+3, point[1]+3],
                        fill=self.RED)

        # Draw time labels under the graph
        label_y = graph_y + graph_height + 8
        for i, time in enumerate(times):
            if i % 2 == 0:  # Show every other label to avoid crowding
                px = x + i * step
                time_text = time.strftime('%I%p').lstrip('0')
                draw.text((px - 15, label_y), time_text, font=self.font_tiny, fill=self.BLACK)

    def draw_forecast(self, draw, forecast_data):
        """Draw 7-day forecast cards"""
        if not forecast_data:
            return

        # Forecast section starts after main section
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
        # Draw card background
        draw.rectangle([x + 2, y, x + width - 2, y + height],
                      outline=self.BLACK, width=1)

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

        # Temperature range
        temp_text = f"{day_data['max_temp']}° / {day_data['min_temp']}°"
        temp_bbox = draw.textbbox((0, 0), temp_text, font=self.font_tiny)
        temp_w = temp_bbox[2] - temp_bbox[0]
        draw.text((x + width // 2 - temp_w // 2, y + 70), temp_text,
                 font=self.font_tiny, fill=self.BLACK)

    def draw_error_message(self, draw, message):
        """Draw error message on display"""
        draw.rectangle([(0, 0), (self.width, self.height)], fill=self.WHITE)

        # Center error message
        y_pos = self.height // 2 - 50
        draw.text((self.PADDING, y_pos), "ERROR", font=self.font_large, fill=self.RED)
        draw.text((self.PADDING, y_pos + 50), message, font=self.font_small, fill=self.BLACK)

        # Timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        draw.text((self.PADDING, self.height - 40), f"Last updated: {timestamp}",
                 font=self.font_tiny, fill=self.BLACK)

    def update_display(self, weather_data):
        """Update the display with weather data"""
        try:
            # Create new image - RGB mode, Inky will convert to palette
            img = Image.new("RGB", (self.width, self.height), (255, 255, 255))
            draw = ImageDraw.Draw(img)

            if not weather_data or not weather_data.get('current'):
                self.draw_error_message(draw, "Unable to fetch weather data. Check your API key and internet connection.")
            else:
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

            # Save for debugging
            img.save('weather_display.png')
            print(f"Weather display saved as weather_display.png at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

            # Display on e-ink
            self.display.set_image(img)
            self.display.show()

            print(f"Weather display updated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        except Exception as e:
            print(f"Error updating display: {e}")
            import traceback
            traceback.print_exc()
            # Try to show error on display
            try:
                img = Image.new("RGB", (self.width, self.height), self.WHITE)
                draw = ImageDraw.Draw(img)
                self.draw_error_message(draw, f"Display error: {str(e)}")
                self.display.set_image(img)
                self.display.show()
            except:
                print("Failed to display error message")

def test_display():
    """Test function to verify display is working"""
    from datetime import timedelta
    try:
        display = WeatherDisplay()
        print("✅ Display initialized successfully")

        # Test with sample data
        test_data = {
            'current': {
                'city': 'Test City',
                'country': 'TC',
                'temperature': 22,
                'feels_like': 25,
                'temp_min': 18,
                'temp_max': 26,
                'description': 'Partly Cloudy',
                'icon': '02d',
                'humidity': 65,
                'wind_speed': 3.2,
                'wind_direction': 180,
                'pressure': 1013,
                'sunrise': datetime.now().replace(hour=6, minute=30),
                'sunset': datetime.now().replace(hour=18, minute=45),
                'visibility': 10.0,
                'uv_index': 5.2,
                'air_quality': {'index': 1, 'description': 'Good'},
                'timestamp': datetime.now()
            },
            'forecast': {
                'hourly': [
                    {'time': datetime.now() + timedelta(hours=i*3), 'temp': 20 + i, 'icon': '02d'}
                    for i in range(8)
                ],
                'daily': [
                    {
                        'date': datetime.now().date() + timedelta(days=i),
                        'day_name': ['Today', 'Fri', 'Sat', 'Sun', 'Mon', 'Tue', 'Wed'][i],
                        'min_temp': 15 + i,
                        'max_temp': 25 + i,
                        'description': 'Sunny',
                        'icon': '01d',
                        'humidity': 50,
                        'wind_speed': 2.1
                    }
                    for i in range(7)
                ]
            },
            'last_updated': datetime.now()
        }

        display.update_display(test_data)
        print("✅ Test display update completed")

    except Exception as e:
        print(f"❌ Display test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_display()
