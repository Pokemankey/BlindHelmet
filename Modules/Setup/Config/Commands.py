import nltk
nltk.download('stopwords')
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from joblib import load

#Module Imports
from Modules.Setup.Config.config import AiName,NLPpath,tfidfPath,MatchPercentage


def getNLPModel():
    nlpModel = load(NLPpath)
    return nlpModel

def getTfidfVectorizer():
    tfidf_vectorizer = load(tfidfPath)
    return tfidf_vectorizer


def evaluateInput(userCommand,nlpModel,tfidf_vectorizer):
    stop_words = set(stopwords.words('english'))
    # Preprocess the input command
    tokenized_command = word_tokenize(userCommand.lower())
    filtered_command = [word for word in tokenized_command if word not in stop_words]
    processed_command = ' '.join(filtered_command)
    
    # Convert command into feature vector
    command_vector = tfidf_vectorizer.transform([processed_command]).toarray()
    
    # Predict action using the trained classifier
    predicted_action = nlpModel.predict(command_vector)
    return predicted_action[0]

#To check if command has a jarvis in it
def ValidCommand(command):
    UserCommand = command.split(' ')
    for i in range(len(UserCommand)):
        if CompareCharacters(UserCommand[i],AiName):
            return True
    return False

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