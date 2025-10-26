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
    base_dir = os.path.dirname(os.path.abspath(__file__))

    model_path = os.path.join(base_dir, 'basic_classifier.pkl')
    vectorizer_path = os.path.join(base_dir, 'count_vectorizer.pkl')

    with open(model_path, 'rb') as fid:
        loaded_model = pickle.load(fid)

    with open(vectorizer_path, 'rb') as vd:
        vectorizer = pickle.load(vd)

    return loaded_model, vectorizer

# Load the model and vectorizer at startup
loaded_model, vectorizer = load_model()

#######################################################
# Define routes
#######################################################

@application.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    color = 'black'

    if request.method == 'POST':
        text = request.form.get('text', '').strip()
        if text:
            text_vectorized = vectorizer.transform([text])
            prediction = loaded_model.predict(text_vectorized)[0]
            color = 'red' if prediction == 'FAKE' else 'green'
    return render_template(
        'index.html',
        prediction=prediction,
        color=color,
        text=text if request.method == 'POST' else ''
    )

@application.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok'}), 200

########################################################
# Run the application
########################################################

if __name__ == "__main__":
    application.run()