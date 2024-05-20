import pytest
from app import app
import time
import json

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_predict(client):
    response = client.post('/predict', json={'text': 'This is a test tweet.'})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'original_message' in data
    assert 'prediction' in data

def test_confirm(client):
    response = client.post('/confirm', json={'is_correct': True, 'original_message': 'This is a test tweet.', 'prediction': 1})
    assert response.status_code == 200
    assert response.data.decode() == "Feedback received"

def test_predict_positive(client):
    # Test positive tweet
    response = client.post('/predict', json={'text': 'This is a great product!'})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'original_message' in data
    assert 'prediction' in data
    assert data['prediction'] == 1 

def test_predict_negative(client):
    # Test negative tweet
    response = client.post('/predict', json={'text': 'I am very disappointed with this product.'})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'original_message' in data
    assert 'prediction' in data
    assert data['prediction'] == 0

def test_predict_speed(client):
    start_time = time.time()
    response = client.post('/predict', json={'text': 'I am very disappointed with this product.'})
    end_time = time.time()
    assert end_time - start_time < 3