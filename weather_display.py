from PIL import Image, ImageDraw, ImageFont
from inky.auto import auto
import textwrap
from datetime import datetime
from config import *

class WeatherDisplay:
    def __init__(self):
        try:
            self.display = auto()
            print(f"Detected display: {self.display.resolution}")
        except Exception as e:
            print(f"Error initializing display: {e}")
            print("Make sure your Inky Impression is properly connected")
            raise
        
        # Set up colors
        self.colors = {
            'black': BLACK,
            'white': WHITE,
            'red': RED,
            'yellow': YELLOW,
            'blue': BLUE,
            'green': GREEN
        }
        
        # Try to load fonts, fallback to default if not available
        try:
            self.title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
            self.large_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
            self.medium_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
            self.small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
        except:
            print("Using default fonts")
            self.title_font = ImageFont.load_default()
            self.large_font = ImageFont.load_default()
            self.medium_font = ImageFont.load_default()
            self.small_font = ImageFont.load_default()
    
    def get_weather_icon(self, icon_code):
        """Map OpenWeatherMap icon codes to simple text representations"""
        icon_map = {
            '01d': '☀',  # clear sky day
            '01n': '🌙',  # clear sky night
            '02d': '⛅',  # few clouds day
            '02n': '☁',  # few clouds night
            '03d': '☁',  # scattered clouds
            '03n': '☁',  # scattered clouds
            '04d': '☁',  # broken clouds
            '04n': '☁',  # broken clouds
            '09d': '🌧',  # shower rain
            '09n': '🌧',  # shower rain
            '10d': '🌦',  # rain day
            '10n': '🌧',  # rain night
            '11d': '⛈',  # thunderstorm
            '11n': '⛈',  # thunderstorm
            '13d': '❄',  # snow
            '13n': '❄',  # snow
            '50d': '🌫',  # mist
            '50n': '🌫',  # mist
        }
        return icon_map.get(icon_code, '🌤')
    
    def draw_current_weather(self, draw, weather_data, y_start=20):
        """Draw current weather information"""
        if not weather_data:
            return y_start
        
        # City and time
        city_text = f"{weather_data['city']}, {weather_data['country']}"
        time_text = weather_data['timestamp'].strftime("%H:%M")
        
        draw.text((20, y_start), city_text, font=self.title_font, fill=self.colors['black'])
        draw.text((20, y_start + 30), time_text, font=self.medium_font, fill=self.colors['black'])
        
        # Main temperature and icon
        temp_text = f"{weather_data['temperature']}°"
        icon = self.get_weather_icon(weather_data['icon'])
        
        # Large temperature
        draw.text((20, y_start + 60), temp_text, font=self.large_font, fill=self.colors['black'])
        draw.text((120, y_start + 60), icon, font=self.large_font, fill=self.colors['black'])
        
        # Description
        desc_text = weather_data['description']
        draw.text((20, y_start + 90), desc_text, font=self.medium_font, fill=self.colors['black'])
        
        # Feels like
        feels_like_text = f"Feels like {weather_data['feels_like']}°"
        draw.text((20, y_start + 110), feels_like_text, font=self.small_font, fill=self.colors['black'])
        
        # Additional details
        details_y = y_start + 140
        if SHOW_HUMIDITY:
            humidity_text = f"Humidity: {weather_data['humidity']}%"
            draw.text((20, details_y), humidity_text, font=self.small_font, fill=self.colors['black'])
            details_y += 20
        
        if SHOW_WIND:
            wind_text = f"Wind: {weather_data['wind_speed']} m/s"
            draw.text((20, details_y), wind_text, font=self.small_font, fill=self.colors['black'])
            details_y += 20
        
        if SHOW_PRESSURE:
            pressure_text = f"Pressure: {weather_data['pressure']} hPa"
            draw.text((20, details_y), pressure_text, font=self.small_font, fill=self.colors['black'])
            details_y += 20
        
        # Sunrise/Sunset
        sunrise_text = f"Sunrise: {weather_data['sunrise'].strftime('%H:%M')}"
        sunset_text = f"Sunset: {weather_data['sunset'].strftime('%H:%M')}"
        draw.text((20, details_y), sunrise_text, font=self.small_font, fill=self.colors['black'])
        draw.text((200, details_y), sunset_text, font=self.small_font, fill=self.colors['black'])
        
        return details_y + 40
    
    def draw_forecast(self, draw, forecast_data, y_start):
        """Draw weather forecast"""
        if not forecast_data or not SHOW_FORECAST:
            return y_start
        
        # Forecast title
        draw.text((20, y_start), "Forecast", font=self.title_font, fill=self.colors['black'])
        y_start += 40
        
        # Draw forecast days
        for i, day in enumerate(forecast_data[:FORECAST_DAYS]):
            x_pos = 20 + (i * 200)  # Space days horizontally
            
            # Day name
            draw.text((x_pos, y_start), day['day_name'], font=self.medium_font, fill=self.colors['black'])
            
            # Icon and description
            icon = self.get_weather_icon(day['icon'])
            draw.text((x_pos, y_start + 25), icon, font=self.medium_font, fill=self.colors['black'])
            draw.text((x_pos + 30, y_start + 25), day['description'], font=self.small_font, fill=self.colors['black'])
            
            # Temperature range
            temp_text = f"{day['max_temp']}°/{day['min_temp']}°"
            draw.text((x_pos, y_start + 45), temp_text, font=self.small_font, fill=self.colors['black'])
            
            # Additional details
            details_text = f"H: {day['humidity']}% W: {day['wind_speed']}m/s"
            draw.text((x_pos, y_start + 65), details_text, font=self.small_font, fill=self.colors['black'])
        
        return y_start + 100
    
    def draw_error_message(self, draw, message):
        """Draw error message on display"""
        # Clear the display
        draw.rectangle([(0, 0), (self.display.width, self.display.height)], fill=self.colors['white'])
        
        # Draw error message
        lines = textwrap.wrap(message, width=40)
        y_pos = 50
        
        for line in lines:
            draw.text((20, y_pos), line, font=self.medium_font, fill=self.colors['black'])
            y_pos += 30
        
        # Draw timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        draw.text((20, y_pos + 20), f"Last updated: {timestamp}", font=self.small_font, fill=self.colors['black'])
    
    def update_display(self, weather_data):
        """Update the display with weather data"""
        try:
            # Create new image
            img = Image.new("RGB", (self.display.width, self.display.height), self.colors['white'])
            draw = ImageDraw.Draw(img)
            
            if not weather_data or not weather_data.get('current'):
                self.draw_error_message(draw, "Unable to fetch weather data. Check your API key and internet connection.")
            else:
                # Draw current weather
                y_pos = self.draw_current_weather(draw, weather_data['current'])
                
                # Draw forecast
                if weather_data.get('forecast'):
                    self.draw_forecast(draw, weather_data['forecast'], y_pos)
                
                # Draw last updated timestamp
                last_updated = weather_data.get('last_updated', datetime.now())
                timestamp_text = f"Last updated: {last_updated.strftime('%H:%M')}"
                draw.text((20, self.display.height - 30), timestamp_text, font=self.small_font, fill=self.colors['black'])
            
            # Display the image
            self.display.set_image(img)
            self.display.show()
            
            print(f"Weather display updated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
        except Exception as e:
            print(f"Error updating display: {e}")
            # Try to show error on display
            try:
                img = Image.new("RGB", (self.display.width, self.display.height), self.colors['white'])
                draw = ImageDraw.Draw(img)
                self.draw_error_message(draw, f"Display error: {str(e)}")
                self.display.set_image(img)
                self.display.show()
            except:
                print("Failed to display error message")

def test_display():
    """Test function to verify display is working"""
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
                'description': 'Partly Cloudy',
                'icon': '02d',
                'humidity': 65,
                'wind_speed': 3.2,
                'pressure': 1013,
                'sunrise': datetime.now().replace(hour=6, minute=30),
                'sunset': datetime.now().replace(hour=18, minute=45),
                'timestamp': datetime.now()
            },
            'forecast': [
                {
                    'date': datetime.now().date() + timedelta(days=1),
                    'day_name': 'Tomorrow',
                    'min_temp': 15,
                    'max_temp': 25,
                    'description': 'Sunny',
                    'icon': '01d',
                    'humidity': 50,
                    'wind_speed': 2.1
                }
            ],
            'last_updated': datetime.now()
        }
        
        display.update_display(test_data)
        print("✅ Test display update completed")
        
    except Exception as e:
        print(f"❌ Display test failed: {e}")

if __name__ == "__main__":
    test_display()
