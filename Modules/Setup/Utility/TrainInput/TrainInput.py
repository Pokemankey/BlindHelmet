import nltk
nltk.download('stopwords')
import random
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report
from joblib import dump


AiName = "Zero"

OCRCommands = [f"read document",
               f"scan document",
               f"read",
               f"read text",
               f"scan text",
               f"can you read this"]

DetectObjectsCommands = [f"find objects",
                         f"detect objects",
                         f"scan objects",
                         f"scan for objects",
                         f"what do you see",
                         f"what is in front of me",]

DetectHumanCommands = [f"find humans",
                       f"detect humans",
                       f"scan humans",
                       f"scan for humans",
                       f"find persons",
                       f"detect persons",
                       f"scan persons",
                       f"scan for persons"]

WeatherCommands = [f" what's the weather like today",
                   f" what is today's weather",
                   f" what's the weather forecast for today",
                   f" can you tell me the weather today",
                   f" tell me today's weather, please",
                   f" what's the forecast today",
                   f" what's the weather today",
                   f" what's the weather report for today",
                   f" what's today's forecast",
                   f" give me the weather for today",
                   f" weather today",
                   f" today's weather"]

youtubeCommands = [f"video player",
                   f"music player",
                   f"start video player",
                   f"start music player",
                   f"open video player",
                   f"open music player"]

resumeCommands = [f"Play",
                   f"resume",
                   f"play music",
                   f"resume music",
                   f"play video",
                   f"resume video"]

pauseCommands = [f"pause",
                   f"pause music",
                   f"pause video"]

exitCommands = [f"exit",
                   f"exit music",
                   f"exit video",
                   f"stop",
                   f"stop music",
                   f"stop video"]

dataset = [
    ("Read Documents", "OCR"),
    ("Scan Objects", "ObjectDetection"),
    ("Find Human", "HumanDetection"),
    ("What is the weather", "WeatherLookup"),
]

dataset += [(command, "OCR") for command in OCRCommands]
dataset += [(command, "ObjectDetection") for command in DetectObjectsCommands]
dataset += [(command, "HumanDetection") for command in DetectHumanCommands]
dataset += [(command, "WeatherLookup") for command in WeatherCommands]
dataset += [(command, "Youtube") for command in youtubeCommands]
dataset += [(command, "resume") for command in resumeCommands]
dataset += [(command, "pause") for command in pauseCommands]
dataset += [(command, "exit") for command in exitCommands]


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
classifier = SVC(kernel='linear')
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
# voice_command = "weather"
# predicted_action = predict_action(voice_command)
# print("Predicted action:", predicted_action)