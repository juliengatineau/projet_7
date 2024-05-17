from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction_text = ""
    error_message = ""
    feedback_message = ""
    if request.method == 'POST':
        X = request.form.get('input')
        if len(X) > 280:
            error_message = "* Cette app ne prédit que les Tweets. Veuillez saisir un message de moins de 280 caractères."
        elif len(X) == 0:
            error_message = "* Veuillez saisir un message."
        else:
            # Send the text to the backend for processing and prediction
            response = requests.post('http://localhost:8001/predict', json={'text': X})
            
            # Convert the response to a Python dictionary
            response_data = response.json()

            # Extract the original message and the prediction
            original_message = response_data['original_message']
            prediction_text = response_data['prediction']

    elif is_correct is not None:
        feedback_message = ["Merci de votre feedback !","Vous pouvez effectuer une nouvelle prédiction"]

        # Send the confirmation to the backend for processing
        response = requests.post('http://localhost:8001/confirm', json={'is_correct': is_correct})

    return render_template('index.html', prediction_text=prediction_text, error_message=error_message, feedback_message=feedback_message, original_message=original_message)

if __name__ == '__main__':
    app.run(port=5000, debug=True)