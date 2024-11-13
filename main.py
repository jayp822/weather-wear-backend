from fastapi import FastAPI, HTTPException

from location_data import LocationData
from smtp_server import get_clothing_recommendations, send_email

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World welcome to weather wear."}


@app.post("/location/{city}/{state}")
async def read_location(city: str, state: str):
    location = LocationData(f"{city}, {state}")
    coordinates = await location.get_coordinates(city, state)
    if "error" in coordinates:
        raise HTTPException(status_code=404, detail="Location not found")
    return {"city": city, "state": state, "coordinates": coordinates}


@app.post("/weather/{city}/{state}")
async def read_weather(city: str, state: str):
    location = LocationData(f"{city}, {state}")
    coordinates = await location.get_coordinates(city, state)
    if "error" in coordinates:
        raise HTTPException(status_code=404, detail="Location not found")

    latitude, longitude = coordinates["latitude"], coordinates["longitude"]
    weather_data = await location.get_weather(latitude, longitude)
    return {
        "city": city,
        "state": state,
        "coordinates": coordinates,
        "weather": weather_data,
    }


@app.post("/send_weather_email/{city}/{state}/{email}")
def send_weather_email(city: str, state: str, email: str):
    location = LocationData(f"{city}, {state}")
    coordinates = location.get_coordinates(city, state)

    if "error" in coordinates:
        raise HTTPException(status_code=404, detail="Location not found")

    latitude = coordinates["latitude"]
    longitude = coordinates["longitude"]

    weather_data = location.get_hourly_for_day(latitude, longitude)

    # if "error" in weather_data:
    #     raise HTTPException(status_code=404, detail="Weather data not found")

    recommendation = get_clothing_recommendations(weather_data)

    # Compose the email body
    subject = f"Clothing Recommendations for {city}, {state}"
    body = f"Here are your clothing recommendations for today:\n\n{recommendation}"

    # Send the email
    send_email(email, subject, body)

    return {"message": "Email sent successfully"}
