#!/usr/bin/env python3
"""
HTML-based Weather Display for Inky Impression
Renders HTML template to image for e-ink display
"""

from PIL import Image
from inky.auto import auto
from datetime import datetime
from jinja2 import Template
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

    def render_html_to_image(self, weather_data):
        """Render HTML template to PIL Image"""

        # Read HTML template
        template_path = 'weather.html'
        if not os.path.exists(template_path):
            raise FileNotFoundError(f"Template file {template_path} not found")

        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()

        # Prepare template data
        template_data = self.prepare_template_data(weather_data)

        # Render template with Jinja2
        template = Template(template_content)
        html_output = template.render(**template_data)

        # Save rendered HTML for debugging
        with open('weather_rendered.html', 'w', encoding='utf-8') as f:
            f.write(html_output)

        # For now, we'll use imgkit or selenium to convert HTML to image
        # Since those require additional setup, let's use a simpler approach
        # We'll import the rendering from html2image if available

        try:
            from html2image import Html2Image
            hti = Html2Image(output_path='.', size=(self.width, self.height))

            # Convert HTML to image
            hti.screenshot(
                html_str=html_output,
                css_file='weather.css',
                save_as='weather_display.png'
            )

            # Load the generated image
            img = Image.open('weather_display.png')
            return img

        except ImportError:
            print("html2image not installed. Falling back to save HTML only.")
            print("Install with: pip3 install html2image")
            print("Also requires Chrome/Chromium to be installed")
            print("\nHTML saved to weather_rendered.html")
            print("You can open this in a browser to preview the dashboard")
            return None

    def prepare_template_data(self, weather_data):
        """Prepare data for HTML template"""
        if not weather_data or not weather_data.get('current'):
            return None

        current = weather_data['current']
        forecast = weather_data.get('forecast', {})

        # Format hourly data for graph
        hourly_data = []
        if forecast.get('hourly'):
            for hour in forecast['hourly'][:11]:  # Take first 11 hours
                hourly_data.append({
                    'time': hour['time'].strftime('%I %p').lstrip('0'),
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
            'temperature': current['temperature'],
            'feels_like': current['feels_like'],
            'temp_high': current['temp_max'],
            'temp_low': current['temp_min'],
            'current_icon': current['icon'],
            'humidity': current['humidity'],
            'wind_speed': current['wind_speed'],
            'pressure': current['pressure'],
            'sunrise': current['sunrise'].strftime('%I:%M %p').lstrip('0'),
            'sunset': current['sunset'].strftime('%I:%M %p').lstrip('0'),
            'visibility': f">{current['visibility']:.1f}" if current['visibility'] >= 10 else f"{current['visibility']:.1f}",
            'uv_index': current.get('uv_index', 0),
            'air_quality': f"{current.get('air_quality', {}).get('index', 0)} /10",
            'hourly_data': hourly_data,
            'temp_min': temp_min,
            'temp_max': temp_max,
            'forecast': forecast.get('daily', [])[:7],
            'last_updated': weather_data.get('last_updated', datetime.now()).strftime('%I:%M%p').lstrip('0')
        }

    def update_display(self, weather_data):
        """Update the display with weather data"""
        try:
            if not weather_data or not weather_data.get('current'):
                print("No weather data available")
                return

            # Render HTML to image
            img = self.render_html_to_image(weather_data)

            if img is None:
                print("Could not render HTML to image")
                print("HTML template saved to weather_rendered.html for preview")
                return

            # Resize if needed to match display
            if img.size != (self.width, self.height):
                img = img.resize((self.width, self.height), Image.Resampling.LANCZOS)

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
                    for i in range(8)
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
