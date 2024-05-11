from Modules.Setup.Config.config import allCommands
from Modules.Setup.VoiceBox.VoiceBoxSetup import speak

def getHelp():
    speak(f"The available commands are : {allCommands}")
