# app.py
from flask import Flask, request
from keras.models import load_model
import dill
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Créer une application Flask
app = Flask(__name__)

# Charger le modèle
model = load_model("model/model.keras")

# Charger le tokenizer
with open('model/tokenizer.dill', 'rb') as f:
    tokenizer = dill.load(f)

# Charger max_seq_len
with open('model/max_seq_len.dill', 'rb') as f:
    max_seq_len = int(dill.load(f))

# Définir une route pour prédire les valeurs
@app.route('/predict', methods=['POST'])

# Fonction pour prédire les valeurs
def predict():
    # Récupérer les données d'entrée au format JSON
    data = request.get_json()
    # Tokenizer les données
    data_tok = tokenizer.texts_to_sequences(data['input'])
    data_tok = pad_sequences(data_tok, maxlen=max_seq_len)
    # Prédire les valeurs
    prediction = model.predict(data_tok)
    # Retourner les valeurs prédites
    return {'prediction': prediction.tolist()}

# Exécuter l'application Flask en mode débogage si le script est exécuté directement
if __name__ == '__main__':
    app.run(debug=True)
