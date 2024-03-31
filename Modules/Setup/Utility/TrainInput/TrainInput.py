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

OCRCommands = [f"{AiName} read document",
               f"{AiName} scan document",
               f"{AiName} read",
               f"{AiName} read text",
               f"{AiName} scan text",
               f"{AiName} can you read this"]

DetectObjectsCommands = [f"{AiName} find objects",
                         f"{AiName} detect objects",
                         f"{AiName} scan objects",
                         f"{AiName} scan for objects",
                         f"{AiName} what do you see",
                         f"{AiName} what is in front of me",]

DetectHumanCommands = [f"{AiName} find humans",
                       f"{AiName} detect humans",
                       f"{AiName} scan humans",
                       f"{AiName} scan for humans",
                       f"{AiName} find persons",
                       f"{AiName} detect persons",
                       f"{AiName} scan persons",
                       f"{AiName} scan for persons"]

WeatherCommands = [f"{AiName}, what's the weather like today",
                   f"{AiName}, what is today's weather",
                   f"{AiName}, what's the weather forecast for today",
                   f"{AiName}, can you tell me the weather today",
                   f"{AiName}, tell me today's weather, please",
                   f"{AiName}, what's the forecast today",
                   f"{AiName}, what's the weather today",
                   f"{AiName}, what's the weather report for today",
                   f"{AiName}, what's today's forecast",
                   f"{AiName}, give me the weather for today",
                   f"{AiName}, weather today",
                   f"{AiName}, today's weather"]

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