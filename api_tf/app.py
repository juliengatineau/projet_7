# app.py
from flask import Flask, request, render_template
import dill
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from applicationinsights import TelemetryClient

# Télécharger les ressources nécessaires pour nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Créer une application Flask
app = Flask(__name__)

# Initialiser le client de télémétrie Application Insights
tc = TelemetryClient('<Your Instrumentation Key>')

# Partie interface utilisateur de l'app
# ---------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    if request.method == 'POST':
        X = request.form.get('input').split('\n')
        X_tok = [transform_bow_with_hash_lem_fct(x) for x in X]
        prediction = model.predict(X_tok)
        # Envoyer une trace à Application Insights
        tc.track_trace('Prediction made')
        tc.flush()
    return render_template('index.html', prediction=prediction)





# Partie prédcition de l'app
# ---------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------


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




# Fonction pour prédire les valeurs
# ---------------------------------------------------------------------------------
# Avoir s'il faudra tester si les données sont valides ici ou plutot au moment de la demande des données voir aussi s'il faut modifier pour des phrases simples plutot que des listes

# Charger le modèle
with open('model/model.dill', 'rb') as f:
    model = dill.load(f)

@app.route('/predict', methods=['POST'])
def predict():
    # Récupérer les données d'entrée au format JSON
    data = request.get_json()
    # Tokenizer les données
    X = data['input']
    X_tok = [transform_bow_with_hash_lem_fct(x) for x in X]

    prediction = model.predict(X_tok)
    # Retourner les valeurs prédites
    return {'prediction': prediction.tolist()}

# Exécuter l'application Flask en mode débogage si le script est exécuté directement
if __name__ == '__main__':
    app.run(debug=True)
