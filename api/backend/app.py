# app.py
from flask import Flask, request, jsonify

import dill
import nltk
from nltk.data import find
import numpy as np
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Créer une application Flask
app = Flask(__name__)

# Fonctions de Tokenizatione et prétraitement du texte et importation des données
# --------------------------------------------------------------------------------


# Télécharger les ressources nécessaires pour nltk
try:
    find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

try:
    find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')


# Tokenizer avec les hashtags
def tokenizer_with_hash_fct(sentence) :
    # print(sentence)
    sentence_clean = sentence.replace('-', ' ').replace('+', ' ').replace('/', ' ')
    word_tokens = word_tokenize(sentence_clean)
    return word_tokens

# Stop words
stop_w = list(set(stopwords.words('english'))) + ['[', ']', ',', '.', ':', '?', '(', ')']

def stop_word_filter_fct(list_words) :
    filtered_w = [w for w in list_words if not w in stop_w]
    filtered_w2 = [w for w in filtered_w if len(w) > 2]
    return filtered_w2

# lower case et alpha
def lower_start_fct(list_words) :
    lw = [w.lower() for w in list_words if (not w.startswith("@")) 
    #                                   and (not w.startswith("#"))
                                       and (not w.startswith("http"))]
    return lw

# Lemmatizer (base d'un mot)
def lemma_fct(list_words) :
    lemmatizer = WordNetLemmatizer()
    lem_w = [lemmatizer.lemmatize(w) for w in list_words]
    return lem_w

# Fonction de préparation du texte pour le bag of words avec lemmatization et hashtags
def transform_bow_with_hash_lem_fct(desc_text) :
    word_tokens = tokenizer_with_hash_fct(desc_text)
    sw = stop_word_filter_fct(word_tokens)
    lw = lower_start_fct(sw)
    lem_w = lemma_fct(lw)    
    transf_desc_text = ' '.join(lem_w)
    return transf_desc_text


# Charger le modèle
try:
    with open('model/model.dill', 'rb') as f:
        model = dill.load(f)

    with open('model/tfidf.dill', 'rb') as f:
        tfidf = dill.load(f)
except Exception as e:
    print(f"Exception occurred while loading the model: {e}")


# Azure insight 
# ---------------------------------------------------------------------------------

# Import the `configure_azure_monitor()` function from the
# `azure.monitor.opentelemetry` package.
from azure.monitor.opentelemetry import configure_azure_monitor
# Import the tracing api from the `opentelemetry` package.
from opentelemetry import trace

import logging

# Configure OpenTelemetry to use Azure Monitor with the 
# APPLICATIONINSIGHTS_CONNECTION_STRING environment variable.
configure_azure_monitor(
    connection_string="InstrumentationKey=2bf5220a-d259-4c2d-9cf8-0d0d19275320;IngestionEndpoint=https://westeurope-5.in.applicationinsights.azure.com/;LiveEndpoint=https://westeurope.livediagnostics.monitor.azure.com/;ApplicationId=acc3a0c5-b7ed-465e-9d2b-56e7f718859a",
)

# Get the current tracer
tracer = trace.get_tracer(__name__)
# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# App
# ---------------------------------------------------------------------------------


@app.route('/predict', methods=['POST'])
def predict():
    X = request.json['text']
    # Process the text here and store the result in a global variable
    # Tokenizer les données
    X_tok = transform_bow_with_hash_lem_fct(X)
    X_tok = tfidf.transform([X_tok])
    result = model.predict(X_tok)

    # Transform the result into an int
    prediction = int(result[0])

    # Return the original message and the prediction
    return jsonify({
        'original_message': X,
        'prediction': prediction
    })


@app.route('/confirm', methods=['POST'])
def confirm():

    is_correct = request.json.get('is_correct')
    original_message = request.json.get('original_message')
    prediction = request.json.get('prediction')

    # Set the custom properties
    custom_properties = {
        'original_message': original_message,
        'prediction': prediction,
        'confirmation': is_correct
    }
    logger.info('message with custom properties', extra=custom_properties)

    return "Feedback received"

# Exécuter l'application Flask en mode débogage si le script est exécuté directement
if __name__ == '__main__':
    app.run(debug=True)
