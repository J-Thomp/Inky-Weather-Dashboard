import requests
import json
from datetime import datetime, timedelta
from config import OPENWEATHER_API_KEY, CITY_NAME, COUNTRY_CODE, UNITS

class WeatherAPI:
    def __init__(self):
        self.api_key = OPENWEATHER_API_KEY
        self.city = CITY_NAME
        self.country = COUNTRY_CODE
        self.units = UNITS
        self.base_url = "http://api.openweathermap.org/data/2.5"
        
        if not self.api_key:
            raise ValueError("OpenWeatherMap API key not found. Please set OPENWEATHER_API_KEY in your .env file")
    
    def get_current_weather(self):
        """Fetch current weather data"""
        url = f"{self.base_url}/weather"
        params = {
            'q': f"{self.city},{self.country}",
            'appid': self.api_key,
            'units': self.units
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            return {
                'temperature': round(data['main']['temp']),
                'feels_like': round(data['main']['feels_like']),
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'wind_speed': data['wind']['speed'],
                'wind_direction': data['wind'].get('deg', 0),
                'description': data['weather'][0]['description'].title(),
                'icon': data['weather'][0]['icon'],
                'city': data['name'],
                'country': data['sys']['country'],
                'sunrise': datetime.fromtimestamp(data['sys']['sunrise']),
                'sunset': datetime.fromtimestamp(data['sys']['sunset']),
                'timestamp': datetime.now()
            }
        except requests.exceptions.RequestException as e:
            print(f"Error fetching current weather: {e}")
            return None
    
    def get_forecast(self, days=3):
        """Fetch weather forecast for specified number of days"""
        url = f"{self.base_url}/forecast"
        params = {
            'q': f"{self.city},{self.country}",
            'appid': self.api_key,
            'units': self.units
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Group forecasts by day
            daily_forecasts = {}
            for item in data['list']:
                date = datetime.fromtimestamp(item['dt']).date()
                if date not in daily_forecasts:
                    daily_forecasts[date] = []
                daily_forecasts[date].append(item)
            
            # Get daily summaries
            forecast_days = []
            for i, (date, day_forecasts) in enumerate(list(daily_forecasts.items())[:days]):
                if i == 0:  # Skip today
                    continue
                    
                # Get min/max temps and most common weather
                temps = [f['main']['temp'] for f in day_forecasts]
                weather_conditions = [f['weather'][0]['description'] for f in day_forecasts]
                
                # Find most common weather condition
                most_common_weather = max(set(weather_conditions), key=weather_conditions.count)
                
                forecast_days.append({
                    'date': date,
                    'day_name': date.strftime('%A'),
                    'min_temp': round(min(temps)),
                    'max_temp': round(max(temps)),
                    'description': most_common_weather.title(),
                    'icon': day_forecasts[0]['weather'][0]['icon'],
                    'humidity': round(sum(f['main']['humidity'] for f in day_forecasts) / len(day_forecasts)),
                    'wind_speed': round(sum(f['wind']['speed'] for f in day_forecasts) / len(day_forecasts), 1)
                })
            
            return forecast_days
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching forecast: {e}")
            return []
    
    def get_weather_data(self):
        """Get both current weather and forecast data"""
        current = self.get_current_weather()
        forecast = self.get_forecast()
        
        return {
            'current': current,
            'forecast': forecast,
            'last_updated': datetime.now()
        }

def test_weather_api():
    """Test function to verify API connection"""
    try:
        weather = WeatherAPI()
        data = weather.get_weather_data()
        
        if data['current']:
            print("✅ Weather API connection successful!")
            print(f"Current temperature in {data['current']['city']}: {data['current']['temperature']}°{UNITS.upper()}")
            print(f"Description: {data['current']['description']}")
        else:
            print("❌ Failed to fetch weather data")
            
    except Exception as e:
        print(f"❌ Error testing weather API: {e}")

if __name__ == "__main__":
    test_weather_api()
