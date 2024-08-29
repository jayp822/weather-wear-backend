import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()


SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
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


def get_clothing_recommendations(hourly_weather_data):
    total_temp = 0
    wind_speed_warning = False
    rain_warning = False

    for hour in hourly_weather_data["hourly"][:24]:
        total_temp += hour["temp"]
        if hour["wind_speed"] > 20:  # Adjust the threshold for windiness as needed
            wind_speed_warning = True
        if "rain" in hour["weather"][0]["description"].lower():
            rain_warning = True

    average_temp = round(total_temp / 24, 2)

    # Base recommendation on average temperature
    if average_temp < 50:
        recommendation = f"It's cold outside today! Wear a coat, gloves, and a warm hat. Average Temperature {average_temp} degrees fahrenheit."
    elif 50 <= average_temp < 68:
        recommendation = f"It's a bit chilly today. A light jacket should be fine. Average Temperature {average_temp} degrees fahrenheit."
    elif 68 <= average_temp < 86:
        recommendation = f"The weather is warm today. T-shirt and jeans would be comfortable. Average Temperature {average_temp} degrees fahrenheit."
    else:
        recommendation = f"It's hot today! Wear shorts and a t-shirt, and don't forget sunscreen. Average Temperature {average_temp} degrees fahrenheit."

    # Additional recommendations based on weather conditions
    if rain_warning:
        recommendation += " It might rain today, so don't forget an umbrella!"
    if wind_speed_warning:
        recommendation += " It's going to be windy today, so wear something that won't easily blow away."

    return recommendation
