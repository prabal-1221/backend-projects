from fastapi import FastAPI, status, HTTPException
import requests
from dotenv import load_dotenv
import os
from typing import Optional
from redis import Redis
import json

load_dotenv()
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')

app = FastAPI()

cache = Redis()

@app.get('/')
def index(city: str, country: str, date1: Optional[str]=None, date2: Optional[str]=None):
    BASE_URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"
    url = ''
    if date1 and date2:
        url = f"{BASE_URL}{city}%2C%20{country}/{date1}/{date2}?unitGroup=metric&key={WEATHER_API_KEY}&contentType=json"
    elif date1:
        url = f"{BASE_URL}{city}%2C%20{country}/{date1}?unitGroup=metric&key={WEATHER_API_KEY}&contentType=json"
    else:
        url = f"{BASE_URL}{city}%2C%20{country}?unitGroup=metric&key={WEATHER_API_KEY}&contentType=json"
    
    if cache.get(url) is not None:
        response_bytes = cache.get(url)
        response_string = response_bytes.decode('utf-8')
        return json.loads(response_string)

    response = requests.get(url)

    if response.status_code == 429:
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Rate limit exceeded. Please try again later.")

    response_string = json.dumps(response.json())
    cache.set(url, response_string)
    return response.json()