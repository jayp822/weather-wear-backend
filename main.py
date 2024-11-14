from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from location_data import LocationData
from smtp_server import get_clothing_recommendations, send_email

app = FastAPI()

origins = [
    "http://localhost:3000",  # for local development, replace with your frontend's URL
    "https://weather-wear-frontend.vercel.app",  # your hosted backend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root FastAPI route"""
    return JSONResponse(
        content={"message": "Weather Wear Backend Working Normally"},
        status_code=status.HTTP_200_OK,
    )


@app.post("/location/{city}/{state}")
async def read_location(city: str, state: str):
    """Takes in city and state as params and returns longitude and latitude coordinates"""
    location = LocationData(f"{city}, {state}")
    coordinates = await location.get_coordinates(city, state)

    if "error" in coordinates:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Location not found"
        )
    return JSONResponse(
        content={"city": city, "state": state, "coordinates": coordinates},
        status_code=status.HTTP_200_OK,
    )


@app.post("/weather/{city}/{state}")
async def read_weather(city: str, state: str):
    """Takes in city and state as params and returns weather conditions"""
    location = LocationData(f"{city}, {state}")
    coordinates = await location.get_coordinates(city, state)
    if "error" in coordinates:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Location not found"
        )

    latitude, longitude = coordinates["latitude"], coordinates["longitude"]
    weather_data = await location.get_weather(latitude, longitude)
    return JSONResponse(
        content={
            "city": city,
            "state": state,
            "coordinates": coordinates,
            "weather": weather_data,
        },
        status_code=status.HTTP_200_OK,
    )


@app.post("/send_weather_email/{city}/{state}/{email}")
def send_weather_email(city: str, state: str, email: str):
    """Takes in city and state as params and sends email to users with clothing recommendations"""
    location = LocationData(f"{city}, {state}")
    coordinates = location.get_coordinates(city, state)

    if "error" in coordinates:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Location not found"
        )

    latitude = coordinates["latitude"]
    longitude = coordinates["longitude"]

    weather_data = location.get_hourly_for_day(latitude, longitude)

    recommendation = get_clothing_recommendations(weather_data)

    city = city.capitalize()
    state = state.capitalize()

    # Compose the email body
    subject = f"Clothing Recommendations for {city}, {state}"
    body = f"Here are your clothing recommendations for today:\n\n{recommendation}\n\n Thank You for Using Weather Wear! - Jay Patel 😃"

    # Send the email
    send_email(email, subject, body)

    return JSONResponse(
        content={"message": "Email Sent Successfully"}, status_code=status.HTTP_200_OK
    )
