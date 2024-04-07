import nltk
nltk.download('stopwords')
nltk.download('punkt')
import random
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report
from joblib import dump
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import confusion_matrix

AiName = "Zero"

objectDetectionCommands = [
    "detect objects",
    "detect objects in the room",
    "detect things",
    "detect for things around me",
    "find objects",
    "find objects in the room",
    "find objects around me",
    "find things",
    "can you look for objects",
    "can you look for things",
    "what objects do you see",
    "what is the closest thing around me",
    "what do you see",
    "what do you see around me",
    "find things for me",
    "find things around me",
    "detect things",
    "detect things around me",
    "find things for me",
    "look for objects",
    "search for objects",
    "search objects",
    "identify objects",
    "locate objects",
    "scan for objects"
]

humanDetectionCommands = [
    "find people",
    "find person",
    "look for people",
    "find humans",
    "is there any human close to me",
    "detect humans",
    "detect humans around me",
    "detect humans in the room",
    "can you look for humans",
    "how many humans do you see",
    "is there any people close to me",
    "detect people",
    "detect people around me",
    "detect people in the room",
    "can you look for people",
    "how many people do you see",
    "is there any person close to me",
    "detect person",
    "detect person around me",
    "detect person in the room",
    "can you look for person",
    "how many person do you see",
    "do you see anyone around",
    "is there someone close to me",
    "search for humans"
]

ocrCommands = [
    "read text",
    "read document",
    "find text",
    "detect text",
    "find document",
    "detect document",
    "scan text",
    "scan document",
    "scan paper",
    "detect paper",
    "can you read this text for me",
    "can you read this document for me",
    "can you scan this document for me",
    "can you scan this text for me",
    "what text do you see",
    "identify text",
    "locate text",
    "read handwriting",
    "scan handwriting",
    "extract text",
    "analyze text",
    "interpret text",
    "decode text",
    "search for text"
]

weatherCommands = [
    "can you tell me what the weather is like today",
    "is it hot outside",
    "is it cold outside",
    "is it sunny outside",
    "what is the weather",
    "what is the weather like",
    "is the weather hot",
    "is the weather cold",
    "is it going to rain today",
    "is it raining",
    "what is the temperature",
    "is the temperature hot",
    "is the temperature cold",
    "weather forecast",
    "weather prediction",
    "weather update",
    "current weather",
    "local weather",
    "weather conditions",
    "weather report",
    "weather outlook",
    "check the weather",
    "weather today",
    "weather information"
]

youtubeCommands = [
    "open video player",
    "open music player",
    "can you play some music for me",
    "open youtube",
    "start video player",
    "start music player",
    "start youtube player",
    "download video",
    "download music",
    "i want to listen to some music",
    "i want to listen to a video",
    "i want to listen to some youtube video",
    "can you play a video for me",
    "load video",
    "load music",
    "play music",
    "play video",
    "start music",
    "start video",
    "watch a video",
    "listen to music",
    "play a song",
    "play a video clip",
    "stream video"
]

resumeCommands = [
    "resume video",
    "resume music",
    "can you resume the music",
    "can you resume the video",
    "resume",
    "continue video",
    "continue music",
    "resume playback",
    "resume from where I left off",
    "start again",
    "resume the video",
    "resume the music",
    "resume playing",
    "resume playback",
    "carry on",
    "pick up where I left off",
    "start from where I stopped",
    "restart video",
    "restart music",
    "resume from pause",
    "resume from stop"
]

pauseCommands = [
    "pause",
    "pause music",
    "pause video",
    "stop music",
    "stop video",
    "stop playing",
    "stop video player",
    "stop music player",
    "stop youtube",
    "stop youtube player",
    "halt",
    "cease",
    "pause playback",
    "hold",
    "freeze",
    "suspend",
    "interrupt",
    "halt music",
    "halt video",
    "pause playback",
    "pause music player",
    "pause video player",
    "pause youtube",
    "pause youtube player"
]

exitCommands = [
    "exit",
    "exit music",
    "exit video",
    "exit music player",
    "exit video player",
    "exit youtube player",
    "quit",
    "quit music",
    "quit video",
    "quit youtube",
    "quit music player",
    "quit video player",
    "quit youtube player",
    "close music",
    "close video",
    "close youtube",
    "close music player",
    "close video player",
    "close youtube player",
    "terminate",
    "end",
    "finish",
    "shutdown",
    "power off",
    "close application",
    "close program",
    "shut down music",
    "shut down video",
    "shut down youtube",
    "shut down music player",
    "shut down video player",
    "shut down youtube player"
]

dateCommands = [
    "what's the date today",
    "current date",
    "today's date",
    "date now",
    "date today",
    "tell me the date",
    "what day is it",
    "get today's date",
    "give me the date",
    "show today's date",
    "date please",
    "current day",
    "current month and date",
    "get the date",
    "today's day",
    "current date and time",
    "what's the current date",
    "current calendar date",
    "date right now",
    "date at this moment",
    "current date and day",
    "date of today",
    "day and date",
    "get date and time",
    "current date and day of the week"
]

helpCommands = [
    "help",
    "show commands",
    "list commands",
    "command list",
    "list available commands",
    "what can you do",
    "available commands",
    "what commands do you have",
    "help me with commands",
    "list all commands",
    "commands list",
    "what are your commands",
    "get commands",
    "list available actions",
    "show me what you can do",
    "commands help",
    "show me commands",
    "show available commands",
    "show all commands",
    "tell me your commands",
    "what do you understand",
    "get available commands",
    "list of commands",
    "available actions",
    "commands available"
]

dataset = []

dataset += [(command, "OCR") for command in ocrCommands]
dataset += [(command, "ObjectDetection") for command in objectDetectionCommands]
dataset += [(command, "HumanDetection") for command in humanDetectionCommands]
dataset += [(command, "WeatherLookup") for command in weatherCommands]
dataset += [(command, "Youtube") for command in youtubeCommands]
dataset += [(command, "Resume") for command in resumeCommands]
dataset += [(command, "Pause") for command in pauseCommands]
dataset += [(command, "Exit") for command in exitCommands]
dataset += [(command, "Date") for command in dateCommands]
dataset += [(command, "Help") for command in helpCommands]



# Tokenize text and remove stopwords
stop_words = set(stopwords.words('english'))
tokenized_dataset = [(word_tokenize(command.lower()), action) for command, action in dataset]
filtered_dataset = [([word for word in words if word not in stop_words], action) for words, action in tokenized_dataset]

# Convert dataset into feature vectors using TF-IDF
corpus = [' '.join(words) for words, _ in filtered_dataset]
tfidf_vectorizer = TfidfVectorizer()
X = tfidf_vectorizer.fit_transform(corpus).toarray()
y = [action for _, action in filtered_dataset]
dump(tfidf_vectorizer, f'{AiName}-tfidf_vectorizer.joblib')

# Split dataset into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train SVM classifier
classifier = GaussianNB()
classifier.fit(X_train, y_train)

# Evaluate the classifier
y_pred = classifier.predict(X_test)
print(classification_report(y_test, y_pred))
dump(classifier, f'{AiName}-NLP.joblib')

# Function to predict action from voice command
def predict_action(command):
    # Preprocess the input command
    tokenized_command = word_tokenize(command.lower())
    filtered_command = [word for word in tokenized_command if word not in stop_words]
    processed_command = ' '.join(filtered_command)
    # Convert command into feature vector
    command_vector = tfidf_vectorizer.transform([processed_command]).toarray()
    # Predict action using the trained classifier
    predicted_action = classifier.predict(command_vector)
    return predicted_action[0]

# Example usage
# voice_command = "lets watch some youtube"
# print(predict_action(voice_command))
# for i in resumeCommands:
#     predicted_action = predict_action(i)
#     print("Predicted action:", predicted_action)
