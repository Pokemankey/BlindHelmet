import requests
from datetime import datetime

# Module Imports
from Modules.Setup.Config.config import UserLocation
from Modules.Setup.VoiceBox.VoiceBoxSetup import speak

def get_weather_forecast():
    try:
        today = datetime.today()
        formatted_date = today.strftime('%Y-%m-%d')
        url = f"https://wttr.in/{UserLocation}?date={formatted_date}&format=%C+%t+%h+%w"
        response = requests.get(url)
        response.raise_for_status()
        weather = response.text.split(' ')
        speak(f"The Weather today is {weather[0]} with a temperature of {weather[1]} and a humidity of {weather[2]}")
        
    except Exception as e:
        speak("Failed to retrieve weather data. Check your wifi connection")
        print(e)
        