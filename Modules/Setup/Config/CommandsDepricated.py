from Modules.Setup.Config.config import AiName,MatchPercentage


OCRCommands = [f"{AiName} read document",f"{AiName} scan document",f"{AiName} read",f"{AiName} read text",f"{AiName} scan text"]
DetectObjectsCommands = [f"{AiName} find objects",f"{AiName} detect objects",f"{AiName} scan objects",f"{AiName} scan for objects"]
DetectHumanCommands = [f"{AiName} find humans",f"{AiName} detect humans",f"{AiName} scan humans",f"{AiName} scan for humans"f"{AiName} find persons",f"{AiName} detect persons",f"{AiName} scan persons",f"{AiName} scan for persons"]

WeatherCommands = [f"{AiName}, what's the weather like today",f"{AiName}, what is today's weather",f"{AiName}, what's the weather forecast for today",f"{AiName}, can you tell me the weather today",f"{AiName}, tell me today's weather, please",f"{AiName}, what's the forecast today",f"{AiName}, what's the weather today",f"{AiName}, what's the weather report for today",f"{AiName}, what's today's forecast",f"{AiName}, give me the weather for today",f"{AiName}, weather today",f"{AiName}, today's weather"]

# To match the user command against every command
def MatchCommand(command):
    UserCommand = command.split(' ')

    if(MatchUserToSystem(UserCommand,OCRCommands)):
        return "OCR"
    elif(MatchUserToSystem(UserCommand,DetectObjectsCommands)):
        return "ObjectDetection"
    elif(MatchUserToSystem(UserCommand,DetectHumanCommands)):
        return "HumanDetection"
    elif(MatchUserToSystem(UserCommand,WeatherCommands)):
        return "Weather"


# To match the user command to system command
def MatchUserToSystem(UserCommand,SystemCommands):
    for i in range(len(SystemCommands)):
        SystemCommand = SystemCommands[i].split(' ')
        wordsCorrect = MatchSentence(UserCommand,SystemCommand)
        percentage = int((wordsCorrect / len(SystemCommand)) * 100)
        print(percentage,SystemCommand)
        if percentage >= MatchPercentage:
            return True 
    return False
    

#To check how many words are similar in 2 sentences
def MatchSentence(UserCommand,SystemCommand):
        L1 = 0
        L2 = 0
        wordsCorrect = 0
        while L1 < len(UserCommand) and L2<len(SystemCommand):
            if CompareCharacters(UserCommand[L1],SystemCommand[L2]):
                wordsCorrect +=1
                L2+=1
            L1+=1
        return wordsCorrect


#To check if command has a jarvis in it
def ValidCommand(command):
    UserCommand = command.split(' ')
    for i in range(len(UserCommand)):
        if CompareCharacters(UserCommand[i],AiName):
            return True
    return False


#To check if 2 words are the same
def CompareWords(word1, word2):
    L1 = 0
    L2 = 0
    while L1 < len(word1) and L2 < len(word2):
        if word1[L1] == word2[L2]:
            L1 += 1
            L2 += 1
        else:
            return False
    return L1 == L2

# compare characters of 2 words , if some % is accurate , return true
def CompareCharacters(userWord,systemWord):
    similarCharacters = 0
    userWordMap = {}
    systemWordMap = {}
    for i in userWord:
        if i in userWordMap:
            userWordMap[i]+=1
        else:
            userWordMap[i]=1
    for i in systemWord:
        if i in systemWordMap:
            systemWordMap[i] +=1
        else:
            systemWordMap[i]=1
    for i in systemWordMap:
        if i in userWordMap:
            if userWordMap[i] > systemWordMap[i]:
                similarCharacters += systemWordMap[i]
            else:
                similarCharacters += userWordMap[i]

    percentage = int((similarCharacters / len(systemWord)) * 100)
    if percentage >= MatchPercentage:
        return True 
    return False