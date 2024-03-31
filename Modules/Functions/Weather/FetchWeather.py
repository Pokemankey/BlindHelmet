import requests
from datetime import datetime
import re

#Module Imports
from Modules.Setup.Config.config import UserLocation
from Modules.Setup.VoiceBox.VoiceBoxSetup import getVoiceBox

def get_weather_forecast():
    engine = getVoiceBox()
    today = datetime.today()
    formatted_date = today.strftime('%Y-%m-%d')
    url = f"https://wttr.in/{UserLocation}?date={formatted_date}&format=%C+%t+%h+%w"
    response = requests.get(url)
    if response.status_code == 200:
        weather = response.text.split(' ')
        engine.say(f"The Weather today is {weather[0]} with a temprature of {weather[1]} and a humidity of {weather[2]}")
        engine.runAndWait()
    else:
        engine.say("Failed to retrieve weather data. No internet Access")
        engine.runAndWait()