import os
from geopy.geocoders import Nominatim
from dotenv import load_dotenv
import requests


load_dotenv()
# load_dotenv("/code/app/.env)

OWM_API_KEY = os.getenv("OPEN_WEATHER_API_KEY")


class LocationData:
    def __init__(self, location_name):
        self.location_name = location_name
        self.geolocator = Nominatim(user_agent="Weather-Wear")

    def get_weather(self, latitude, longitude):
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={OWM_API_KEY}&units=imperial"
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            weather_data = response.json()
            return {
                "temperature": weather_data["main"]["temp"],
                "weather": weather_data["weather"][0]["description"],
                "humidity": weather_data["main"]["humidity"],
                "wind_speed": weather_data["wind"]["speed"],
            }
        else:
            return {"error": "Unable to fetch weather data"}

    def get_hourly_for_day(self, latitude, longitude):
        url = f"https://api.openweathermap.org/data/2.5/onecall?lat={latitude}&lon={longitude}&exclude=current,minutely,daily,alerts&appid={OWM_API_KEY}&units=imperial"

        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            weather_data = response.json()
            return weather_data  # Return the entire weather data dictionary
        else:
            return {"error": "Unable to fetch weather data"}

    def get_coordinates(self, city, state):
        # Use the geolocator to get coordinates for the specified city and state
        location = self.geolocator.geocode(f"{city}, {state}")
        if location:
            return {"latitude": location.latitude, "longitude": location.longitude}
        else:
            return {"error": "Location not found"}
