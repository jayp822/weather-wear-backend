import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv

load_dotenv()

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = os.getenv("SMTP_PORT")
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


def send_email(recipient_email, subject, body):
    try:
        # Create a MIME object
        msg = MIMEMultipart()
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = recipient_email
        msg["Subject"] = subject

        # Attach the email body
        msg.attach(MIMEText(body, "plain"))

        # Establish a connection to the SMTP server
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Secure the connection
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        # Send the email
        server.send_message(msg)
        server.quit()

        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")


def get_clothing_recommendations(weather_json):

    # Access the first forecast item in the list for current weather conditions
    current_weather = weather_json["list"][0]
    temperature = current_weather["main"]["temp"]
    feels_like = current_weather["main"]["feels_like"]
    weather_description = current_weather["weather"][0]["description"]
    wind_speed = current_weather["wind"]["speed"]

    # Print data for debugging
    print(
        f"Temperature: {temperature}, Feels like: {feels_like}, Description: {weather_description}, Wind speed: {wind_speed}"
    )

    # Clothing recommendation logic based on temperature and description
    if "clear" in weather_description.lower():
        if temperature > 30:
            recommendation = "It's hot outside. Wear lightweight clothing, sunglasses, and sunscreen."
        elif 20 <= temperature <= 30:
            recommendation = (
                "The weather is warm. A light shirt and shorts would be perfect."
            )
        elif 10 <= temperature < 20:
            recommendation = (
                "It's a bit cool. Consider wearing a light jacket or sweater."
            )
        else:
            recommendation = "It's cold. Make sure to bundle up with a warm jacket."
    elif "clouds" in weather_description.lower():
        if temperature > 25:
            recommendation = "It might be cloudy but still warm. A light jacket or t-shirt should be fine."
        elif 15 <= temperature <= 25:
            recommendation = "Cloudy weather, so wear a jacket or sweater for comfort."
        else:
            recommendation = "Cool and cloudy, wear a warm jacket or coat."
    elif "snow" in weather_description.lower():
        recommendation = "Snowing! Dress warmly with a heavy coat, gloves, and scarf."
    elif "rain" in weather_description.lower():
        recommendation = "It's rainy. A waterproof jacket and umbrella are recommended."
    else:
        recommendation = (
            "The weather seems unpredictable. Layer up to stay comfortable."
        )

    # Wind speed recommendation
    if wind_speed > 10:
        recommendation += " Be mindful of strong winds; consider wearing something that shields you from the wind."

    return recommendation
