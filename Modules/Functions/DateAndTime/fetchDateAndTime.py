from datetime import datetime
from Modules.Setup.VoiceBox.VoiceBoxSetup import getVoiceBox

def get_current_datetime():
    engine = getVoiceBox()
    today = datetime.today()
    day = today.strftime('%d').lstrip('0') 
    formatted_date = today.strftime(f'{day}th/%B/%Y, %A, %I:%M %p')
    engine.say(f"The current date and time is {formatted_date}")
    engine.runAndWait()
