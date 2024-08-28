# main.py
# Run the server with: uvicorn main:app --reload

from urllib.parse import unquote
from fastapi import FastAPI, HTTPException
from smtp_server import send_email, get_clothing_recommendations
from location_data import LocationData


app = FastAPI()

# if __name__ == "__main__":
#     import uvicorn

#     uvicorn.run(app, host="0.0.0.0", port=8000)


@app.get("/")
async def root():
    return {"message": "Hello World welcome to weather wear."}


@app.post("/location/{city}/{state}")
async def read_location(city: str, state: str):
    # Create an object of LocationData
    location = LocationData(f"{city}, {state}")

    # Get the coordinates of the location
    coordinates = location.get_coordinates(city, state)

    if "error" not in coordinates:
        return {"city": city, "state": state, "coordinates": coordinates}
    else:
        return {"error": "Location not found"}


@app.post("/weather/{city}/{state}")
async def read_weather(city: str, state: str):
    # Create an object of LocationData
    location = LocationData(f"{city}, {state}")

    # Get the coordinates of the location
    coordinates = location.get_coordinates(city, state)

    if "error" in coordinates:
        return {"error": "Location not found"}

    latitude = coordinates["latitude"]
    longitude = coordinates["longitude"]

    weather_data = location.get_weather(latitude, longitude)

    # Placeholder for integrating with a weather API using the latitude and longitude
    # For now, we'll return the coordinates
    return {
        "city": city,
        "state": state,
        "coordinates": coordinates,
        "weather": weather_data,
    }


@app.post("/send_weather_email/{city}/{state}/{email}")
async def send_weather_email(city: str, state: str, email: str):
    location = LocationData(f"{city}, {state}")
    coordinates = location.get_coordinates(city, state)

    if "error" in coordinates:
        raise HTTPException(status_code=404, detail="Location not found")

    latitude = coordinates["latitude"]
    longitude = coordinates["longitude"]

    hourly_weather_data = location.get_hourly_for_day(latitude, longitude)

    if "error" in hourly_weather_data:
        raise HTTPException(status_code=404, detail="Weather data not found")

    recommendation = get_clothing_recommendations(hourly_weather_data)

    # Compose the email body
    subject = f"Clothing Recommendations for {city}, {state}"
    body = f"Here are your clothing recommendations for today:\n\n{recommendation}"

    # Send the email
    send_email(email, subject, body)

    return {"message": "Email sent successfully"}


@app.post("/send_weather_average/{city}/{state}")
async def send_weather_email(city: str, state: str):
    location = LocationData(f"{city}, {state}")
    coordinates = location.get_coordinates(city, state)

    if "error" in coordinates:
        raise HTTPException(status_code=404, detail="Location not found")

    latitude = coordinates["latitude"]
    longitude = coordinates["longitude"]

    weather_data = location.get_hourly_for_day(latitude, longitude)

    if "error" in weather_data:
        raise HTTPException(status_code=404, detail="Weather data not found")

    return weather_data  # Return the entire weather data
