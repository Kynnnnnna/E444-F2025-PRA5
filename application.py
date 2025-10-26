from flask import Flask, request, jsonify, render_template
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import pickle
import os

application = Flask(__name__)

########################################################
# Function to load the model and vectorizer
########################################################

# Function to load the model
def load_model():
    loaded_model = None
    with open('basic_classifier.pkl', 'rb') as fid:
        loaded_model = pickle.load(fid)
    vectorizer = None
    with open('count_vectorizer.pkl', 'rb') as vd:
        vectorizer = pickle.load(vd)
    return loaded_model, vectorizer

loaded_model, vectorizer = load_model()

#######################################################
# Define routes
#######################################################

@application.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    color = 'black'
    text = ''

    if request.method == 'POST':
        text = request.form.get('text', '').strip()
        if text:
            prediction = loaded_model.predict(vectorizer.transform([text]))[0]
            color = 'red' if prediction == 'FAKE' else 'green'
    return render_template(
        'index.html',
        prediction=prediction,
        color=color,
        text=text
    )

@application.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok'}), 200

########################################################
# Run the application
########################################################

if __name__ == "__main__":
    application.run()