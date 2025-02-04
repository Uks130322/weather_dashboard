# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv
from cors import setup_cors  # Import CORS setting

load_dotenv()
app = FastAPI()

setup_cors(app)


class WeatherResponse(BaseModel):
    city: str
    country: str
    temperature: float
    weather_description: str
    icon: str


# Endpoint for get weather
@app.get("/weather/{city}", response_model=WeatherResponse)
async def get_weather(city: str):
    api_key = os.getenv("OPENWEATHERMAP_API_KEY")
    if not api_key or api_key == "":
        raise HTTPException(status_code=500, detail="API key not configured")

    # Request to OpenWeatherMap API
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="City not found")

    data = response.json()
    weather_info = {
        "city": data["name"],
        "country": data["sys"]["country"],
        "temperature": data["main"]["temp"],
        "weather_description": data["weather"][0]["description"],
        "icon": data["weather"][0]["icon"],
    }
    return weather_info


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
