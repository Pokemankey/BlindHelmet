from Modules.Setup.Config.config import allCommands
from Modules.Setup.VoiceBox.VoiceBoxSetup import getVoiceBox

def getHelp():
    engine = getVoiceBox()
    engine.say(f"The available commands are : {allCommands}")
    engine.runAndWait()
