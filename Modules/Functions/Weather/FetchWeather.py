import requests
from datetime import datetime

# Module Imports
from Modules.Setup.Config.config import UserLocation
from Modules.Setup.VoiceBox.VoiceBoxSetup import getVoiceBox

def get_weather_forecast():
    engine = getVoiceBox()
    try:
        today = datetime.today()
        formatted_date = today.strftime('%Y-%m-%d')
        url = f"https://wttr.in/{UserLocation}?date={formatted_date}&format=%C+%t+%h+%w"
        response = requests.get(url)
        response.raise_for_status()
        weather = response.text.split(' ')
        engine.say(f"The Weather today is {weather[0]} with a temperature of {weather[1]} and a humidity of {weather[2]}")
        engine.runAndWait()
    except Exception as e:
        engine.say("Failed to retrieve weather data. Check your wifi connection")
        print(e)
        engine.runAndWait()