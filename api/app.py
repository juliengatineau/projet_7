# app.py
from flask import Flask, request, jsonify
import dill
import nltk
from nltk.data import find
import numpy as np
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from applicationinsights import TelemetryClient

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


# Fonctions de Tokenizatione et prétraitement du texte
# ---------------------------------------------------------------------------------

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
with open('model/model.dill', 'rb') as f:
    model = dill.load(f)

with open('model/tfidf.dill', 'rb') as f:
    tfidf = dill.load(f)


# Créer une application Flask
app = Flask(__name__, template_folder='frontend/templates')

# Initialiser le client de télémétrie Application Insights
#tc = TelemetryClient('<Your Instrumentation Key>')
# Partie interface utilisateur de l'app
# ---------------------------------------------------------------------------------

@app.route('/predict', methods=['POST'])
def predict():
    X = request.json['text']
    # Process the text here and store the result in a global variable
    # Tokenizer les données
    X_tok = transform_bow_with_hash_lem_fct(X)
    X_tok = tfidf.transform([X_tok])
    result = model.predict(X_tok)

    # Transform the result into a sentence
    prediction = "Votre tweet a été prédit positif." if result[0] == 1 else "Votre tweet a été prédit négatif."

    # Return the original message and the prediction
    return jsonify({
        'original_message': X,
        'prediction': prediction
    })

@app.route('/confirm', methods=['POST'])
def confirm():
    is_correct = request.form.get('is_correct')
    if is_correct == 'oui':
        is_correct = True
    elif is_correct == 'non':
        is_correct = False
    return "True"

# Exécuter l'application Flask en mode débogage si le script est exécuté directement
if __name__ == '__main__':
    app.run(debug=True)
