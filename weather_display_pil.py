#!/usr/bin/env python3
"""
PIL-based Weather Display for Inky Impression
Renders weather dashboard with actual PNG icons to match HTML design
"""

from PIL import Image, ImageDraw, ImageFont
from inky.auto import auto
from datetime import datetime
import os

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

        # Colors - use grayscale for better e-ink rendering
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GRAY_LIGHT = (245, 245, 245)
        self.GRAY_MID = (153, 153, 153)
        self.GRAY_DARK = (102, 102, 102)
        self.BORDER = (221, 221, 221)

        # Try to load fonts
        try:
            self.font_location = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 28)
            self.font_date = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
            self.font_temp_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 52)
            self.font_temp_unit = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)
            self.font_feels = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
            self.font_detail_label = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 11)
            self.font_detail_value = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 15)
            self.font_forecast_day = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 13)
            self.font_forecast_temp = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 11)
            self.font_axis = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 9)
            self.font_footer = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 9)
        except Exception as e:
            print(f"Warning: Could not load fonts: {e}")
            print("Using default fonts")
            # Fallback to default
            self.font_location = ImageFont.load_default()
            self.font_date = ImageFont.load_default()
            self.font_temp_large = ImageFont.load_default()
            self.font_temp_unit = ImageFont.load_default()
            self.font_feels = ImageFont.load_default()
            self.font_detail_label = ImageFont.load_default()
            self.font_detail_value = ImageFont.load_default()
            self.font_forecast_day = ImageFont.load_default()
            self.font_forecast_temp = ImageFont.load_default()
            self.font_axis = ImageFont.load_default()
            self.font_footer = ImageFont.load_default()

    def load_icon(self, icon_name, size):
        """Load and resize an icon"""
        icon_path = f"icons/{icon_name}.png"
        if not os.path.exists(icon_path):
            print(f"Warning: Icon {icon_path} not found")
            # Return a blank image
            return Image.new('RGBA', (size, size), (255, 255, 255, 0))

        try:
            icon = Image.open(icon_path)
            # Convert to RGBA if needed
            if icon.mode != 'RGBA':
                icon = icon.convert('RGBA')
            # Resize maintaining aspect ratio
            icon.thumbnail((size, size), Image.Resampling.LANCZOS)
            return icon
        except Exception as e:
            print(f"Error loading icon {icon_path}: {e}")
            return Image.new('RGBA', (size, size), (255, 255, 255, 0))

    def draw_header(self, draw, city, country, current_date):
        """Draw centered header with location and date"""
        # Location
        location = f"{city}, {country}"
        bbox = draw.textbbox((0, 0), location, font=self.font_location)
        text_width = bbox[2] - bbox[0]
        x = (self.width - text_width) // 2
        draw.text((x, 15), location, font=self.font_location, fill=self.BLACK)

        # Date
        bbox = draw.textbbox((0, 0), current_date, font=self.font_date)
        text_width = bbox[2] - bbox[0]
        x = (self.width - text_width) // 2
        draw.text((x, 48), current_date, font=self.font_date, fill=self.GRAY_DARK)

    def draw_current_weather(self, img, draw, weather_data, y_start=70):
        """Draw current weather section with icon and temperature"""
        current = weather_data['current']

        # Left side - Large icon (130x130)
        icon = self.load_icon(current['icon'], 130)
        img.paste(icon, (35, y_start), icon if icon.mode == 'RGBA' else None)

        # Temperature next to icon
        temp_x = 185
        temp_y = y_start + 20

        # Main temperature
        temp_text = f"{current['temperature']}°"
        draw.text((temp_x, temp_y), temp_text, font=self.font_temp_large, fill=self.BLACK)

        # Unit (smaller, superscript-ish)
        bbox = draw.textbbox((temp_x, temp_y), temp_text, font=self.font_temp_large)
        unit_x = bbox[2] - 25  # Position after temperature
        draw.text((unit_x, temp_y + 8), "F", font=self.font_temp_unit, fill=self.BLACK)

        # Feels like
        feels_text = f"Feels Like {current['feels_like']}°"
        draw.text((temp_x, temp_y + 70), feels_text, font=self.font_feels, fill=self.GRAY_DARK)

    def draw_details(self, img, draw, weather_data, y_start=70):
        """Draw two columns of weather details with icons"""
        current = weather_data['current']

        # Column positions
        col1_x = 375
        col2_x = 575
        detail_y = y_start
        row_spacing = 44

        # Column 1 details
        details_col1 = [
            ('sunrise', 'Sunrise', current['sunrise'].strftime('%I:%M %p').lstrip('0')),
            ('wind', 'Wind', f"{current['wind_speed']} mph"),
            ('visibility', 'Visibility', f"{current.get('visibility', 10):.1f} mi"),
        ]

        # Column 2 details
        details_col2 = [
            ('sunset', 'Sunset', current['sunset'].strftime('%I:%M %p').lstrip('0')),
            ('humidity', 'Humidity', f"{current['humidity']} %"),
            ('aqi', 'Air Quality', f"{current.get('air_quality', {}).get('index', 0)} /10"),
        ]

        # Draw column 1
        for i, (icon_name, label, value) in enumerate(details_col1):
            y = detail_y + i * row_spacing
            # Load and paste icon (26x26)
            icon = self.load_icon(icon_name, 26)
            img.paste(icon, (col1_x, y + 5), icon if icon.mode == 'RGBA' else None)
            # Draw label and value
            draw.text((col1_x + 41, y), label, font=self.font_detail_label, fill=self.GRAY_MID)
            draw.text((col1_x + 41, y + 14), value, font=self.font_detail_value, fill=self.BLACK)

        # Draw column 2
        for i, (icon_name, label, value) in enumerate(details_col2):
            y = detail_y + i * row_spacing
            # Load and paste icon (26x26)
            icon = self.load_icon(icon_name, 26)
            img.paste(icon, (col2_x, y + 5), icon if icon.mode == 'RGBA' else None)
            # Draw label and value
            draw.text((col2_x + 41, y), label, font=self.font_detail_label, fill=self.GRAY_MID)
            draw.text((col2_x + 41, y + 14), value, font=self.font_detail_value, fill=self.BLACK)

    def draw_graph_section(self, draw, hourly_data, temp_min, temp_max, y_start=215):
        """Draw temperature graph with time labels"""
        if not hourly_data or len(hourly_data) < 2:
            return

        # Graph dimensions
        graph_x = 60
        graph_width = 680
        graph_height = 70
        graph_y = y_start + 10

        # Background
        draw.rectangle([15, y_start, self.width - 15, y_start + 95],
                      fill=self.WHITE, outline=self.BORDER, width=1)

        # Y-axis labels (left - temperature)
        draw.text((20, graph_y), f"{temp_max}°F", font=self.font_axis, fill=self.GRAY_DARK)
        draw.text((20, graph_y + graph_height - 10), f"{temp_min}°F", font=self.font_axis, fill=self.GRAY_DARK)

        # Y-axis labels (right - rain %)
        draw.text((self.width - 45, graph_y), "100%", font=self.font_axis, fill=self.GRAY_DARK)
        draw.text((self.width - 38, graph_y + graph_height - 10), "0%", font=self.font_axis, fill=self.GRAY_DARK)

        # Calculate points for temperature line
        temps = [h['temp'] for h in hourly_data]
        temp_range = temp_max - temp_min if temp_max != temp_min else 1

        points = []
        step = graph_width / (len(temps) - 1) if len(temps) > 1 else graph_width

        for i, temp in enumerate(temps):
            px = graph_x + i * step
            # Invert y (higher temp = higher on screen)
            py = graph_y + graph_height - ((temp - temp_min) / temp_range) * graph_height
            points.append((int(px), int(py)))

        # Draw temperature line with orange color
        ORANGE = (255, 140, 66)
        if len(points) > 1:
            draw.line(points, fill=ORANGE, width=2)

        # Draw points
        for point in points:
            draw.ellipse([point[0]-3, point[1]-3, point[0]+3, point[1]+3],
                        fill=ORANGE, outline=self.BLACK, width=1)

        # Time labels below graph
        label_y = graph_y + graph_height + 8
        for i, hour in enumerate(hourly_data):
            if i % 2 == 0:  # Every other label
                px = graph_x + i * step
                time_text = hour['time']
                bbox = draw.textbbox((0, 0), time_text, font=self.font_axis)
                text_width = bbox[2] - bbox[0]
                draw.text((int(px - text_width // 2), label_y), time_text,
                         font=self.font_axis, fill=self.GRAY_DARK)

    def draw_forecast(self, img, draw, forecast_data, y_start=315):
        """Draw 7-day forecast cards"""
        if not forecast_data:
            return

        daily_forecasts = forecast_data[:7]
        if not daily_forecasts:
            return

        # Calculate card dimensions
        cards_per_row = len(daily_forecasts)
        total_spacing = 15 * 2  # Left and right padding
        gap_spacing = 6 * (cards_per_row - 1)
        available_width = self.width - total_spacing - gap_spacing
        card_width = available_width // cards_per_row
        card_height = 100

        for i, day in enumerate(daily_forecasts):
            card_x = 15 + i * (card_width + 6)
            self.draw_forecast_card(img, draw, day, card_x, y_start, card_width, card_height)

    def draw_forecast_card(self, img, draw, day_data, x, y, width, height):
        """Draw a single forecast card"""
        # Card background with border
        draw.rectangle([x, y, x + width, y + height],
                      fill=self.WHITE, outline=self.GRAY_MID, width=2)

        # Day name (centered)
        day_name = day_data['day_name']
        bbox = draw.textbbox((0, 0), day_name, font=self.font_forecast_day)
        text_width = bbox[2] - bbox[0]
        draw.text((x + (width - text_width) // 2, y + 8), day_name,
                 font=self.font_forecast_day, fill=self.BLACK)

        # Weather icon (centered, 40x40)
        icon = self.load_icon(day_data['icon'], 40)
        icon_x = x + (width - 40) // 2
        icon_y = y + 30
        img.paste(icon, (icon_x, icon_y), icon if icon.mode == 'RGBA' else None)

        # Temperature range (centered)
        temp_text = f"{day_data['max_temp']} / {day_data['min_temp']}°"
        bbox = draw.textbbox((0, 0), temp_text, font=self.font_forecast_temp)
        text_width = bbox[2] - bbox[0]
        draw.text((x + (width - text_width) // 2, y + 78), temp_text,
                 font=self.font_forecast_temp, fill=self.BLACK)

    def prepare_template_data(self, weather_data):
        """Prepare data for display rendering"""
        if not weather_data or not weather_data.get('current'):
            return None

        current = weather_data['current']
        forecast = weather_data.get('forecast', {})

        # Format hourly data for graph
        hourly_data = []
        if forecast.get('hourly'):
            for hour in forecast['hourly'][:11]:  # Take first 11 hours
                hourly_data.append({
                    'time': hour['time'].strftime('%I %p').lstrip('0').lower(),
                    'temp': hour['temp'],
                    'rain_chance': 0  # Need to add rain chance to API data
                })

        # Calculate temp range for graph scaling
        temps = [h['temp'] for h in hourly_data] if hourly_data else [current['temperature']]
        temp_min = min(temps)
        temp_max = max(temps)

        # Format state code (convert country to state if US)
        state = current.get('country', 'US')
        if state == 'US':
            state = 'PA'  # Default to PA for Conshohocken

        return {
            'city': current['city'],
            'country': state,
            'current_date': current['timestamp'].strftime('%A, %B %d'),
            'current': current,
            'hourly_data': hourly_data,
            'temp_min': temp_min,
            'temp_max': temp_max,
            'forecast': forecast.get('daily', [])[:7],
            'last_updated': weather_data.get('last_updated', datetime.now()).strftime('%I:%M%p').lstrip('0').lower()
        }

    def update_display(self, weather_data):
        """Update the display with weather data"""
        try:
            if not weather_data or not weather_data.get('current'):
                print("No weather data available")
                return

            # Prepare data
            data = self.prepare_template_data(weather_data)
            if not data:
                print("Could not prepare template data")
                return

            # Create image with light gray background
            img = Image.new("RGB", (self.width, self.height), self.GRAY_LIGHT)
            draw = ImageDraw.Draw(img)

            # Draw all sections
            self.draw_header(draw, data['city'], data['country'], data['current_date'])
            self.draw_current_weather(img, draw, data, y_start=70)
            self.draw_details(img, draw, data, y_start=70)
            self.draw_graph_section(draw, data['hourly_data'], data['temp_min'], data['temp_max'], y_start=215)
            self.draw_forecast(img, draw, data['forecast'], y_start=315)

            # Footer - last updated
            footer_text = data['last_updated']
            bbox = draw.textbbox((0, 0), footer_text, font=self.font_footer)
            text_width = bbox[2] - bbox[0]
            draw.text((self.width - text_width - 15, self.height - 15), footer_text,
                     font=self.font_footer, fill=self.GRAY_MID)

            # Save for debugging
            img.save('weather_display.png')
            print(f"Weather display saved as weather_display.png")

            # Display on e-ink
            self.display.set_image(img)
            self.display.show()

            print(f"Weather display updated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        except Exception as e:
            print(f"Error updating display: {e}")
            import traceback
            traceback.print_exc()


def test_display():
    """Test function to verify display is working"""
    from datetime import timedelta
    try:
        display = WeatherDisplay()
        print("✅ Display initialized successfully")

        # Test with sample data
        test_data = {
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
                'air_quality': {'index': 2, 'description': 'Fair'},
                'timestamp': datetime.now()
            },
            'forecast': {
                'hourly': [
                    {'time': datetime.now() + timedelta(hours=i*3), 'temp': 50 + i, 'icon': '02d'}
                    for i in range(11)
                ],
                'daily': [
                    {
                        'date': datetime.now().date() + timedelta(days=i),
                        'day_name': ['Fri', 'Sat', 'Sun', 'Mon', 'Tue', 'Wed', 'Thu'][i],
                        'min_temp': 46 + i,
                        'max_temp': 54 + i,
                        'description': 'Partly Cloudy',
                        'icon': '02d',
                        'humidity': 60,
                        'wind_speed': 5.99
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
