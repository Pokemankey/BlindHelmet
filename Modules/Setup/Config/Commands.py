#Module Imports
from Modules.Setup.Config.config import AiName

def evaluateInput(userCommand, db):
    results = db.similarity_search_with_score(userCommand, k=1)
    predicted_action = "".join([doc.page_content for doc, _score in results if _score < 1.5])
    if len(predicted_action) == 0:
        return "None"
    return predicted_action.split(" ")[0]

#To check if command has a jarvis in it
def ValidCommand(command):
    UserCommand = command.split(' ')
    for i in range(len(UserCommand)):
        if CompareCharacters(UserCommand[i],AiName,100):
            return True
    return False

#To check if command has a jarvis in it
def ValidGeminiCommand(command):
    UserCommand = command.split(' ')
    for i in range(len(UserCommand)):
        if CompareCharacters(UserCommand[i],"gemini",60):
            return True
    return False

# compare characters of 2 words , if some % is accurate , return true
def CompareCharacters(userWord,systemWord,matchPercentage):
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
    if percentage >= matchPercentage:
        return True 
    return False