from flask_testing import TestCase
from api_projet7 import app

# Créer une classe de test pour tester l'API
class TestAPI(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app
    

    # Tester la route /predict
    def test_predict(self):
        # Envoyer une requête POST à la route /predict
        response = self.client.post('/predict', json={'input': ["Une super journée", "C'est vraiment la merde, horrible", "Je t'aime de tout mon coeur"]})
        # Vérifier que la requête a réussi
        self.assertEqual(response.status_code, 200)
        # Vérifier que la réponse contient une prédiction.
        json_data = response.get_json()
        self.assertIn('prediction', json_data)