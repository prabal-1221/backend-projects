import requests
from dotenv import load_dotenv
import os

load_dotenv()

WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')


response = requests.get(f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Pune%2C%20India/2025-01-01/2025-01-09?unitGroup=metric&key={WEATHER_API_KEY}&contentType=json')

print(response.json())