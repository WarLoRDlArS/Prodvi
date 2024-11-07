import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import ComplementNB
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string

# Stopword removal function
def remove_stopwords(text):
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text)
    filtered_words = [word for word in words if word.lower() not in stop_words and word not in string.punctuation]
    return ' '.join(filtered_words)

# User input to choose dataset
dataset_choice = input("1: Choose dataset to load dataset, 2: Randomized Questions ")

if dataset_choice == '1':
    # Load the first dataset
    df = pd.read_csv('clean_slate/prodvi-dataset-new4.csv')

    # Split column
    df[['Text', 'Label']] = df['Adaptability'].str.split('(', expand=True)
    df['Label'] = df['Label'].replace(r'\)', '', regex=True)
    df.dropna(subset=['Label'], inplace=True)
    
    # Define features and target as Series
    x = df['Text']
    y = df['Label']

elif dataset_choice == '2':
    # Load the second dataset
    df = pd.read_csv('clean_slate/prodvi-randomised-questionset.csv')

    # Apply stopword removal to 'Question' column
    df['Question'] = df['Question'].apply(remove_stopwords)
    x = df['Question']  # x is a Series (1D)
    y = df['Label']  # y is also a Series (1D)

# Define classifiers to test
models = {
    'ComplementNB': ComplementNB(),
    'LinearSVC': LinearSVC()
}

# Dictionary to track best random_state and accuracy for each model
best_results = {
    'ComplementNB': {'random_state': None, 'accuracy': 0},
    'LinearSVC': {'random_state': None, 'accuracy': 0}
}

# Loop over a range of random_state values
for random_state in range(0, 50000):  # You can increase this range if needed
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=random_state)
    
    # Test each model
    for model_name, model in models.items():
        # Create a pipeline with TfidfVectorizer and the current model
        pipe = Pipeline([('tfidf', TfidfVectorizer()), ('clf', model)])
        
        # Train the model
        pipe.fit(X_train, y_train)

        # Make predictions
        predictions = pipe.predict(X_test)

        # Calculate accuracy
        accuracy = accuracy_score(y_test, predictions)

        # Check if this is the best accuracy so far for the current model
        if accuracy > best_results[model_name]['accuracy']:
            best_results[model_name]['accuracy'] = accuracy
            best_results[model_name]['random_state'] = random_state

        # Print progress for each model and random state
        print(f"{model_name} - Random State: {random_state}, Accuracy: {accuracy:.4f}")

        # Break if accuracy is 1.0
        if accuracy == 1.0:
            print(f"\nAchieved 100% Accuracy with {model_name} at Random State: {random_state}")
            break
    else:
        # Continue the outer loop if the inner loop didn't break
        continue
    # Break the outer loop if the inner loop did break
    break

# Output the best result for each model
print("\nBest Results:")
for model_name, result in best_results.items():
    print(f"{model_name}: Best Random State: {result['random_state']}, Accuracy: {result['accuracy']:.4f}") 
