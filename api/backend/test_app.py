import pytest
from flask import Flask
from app import app
import time

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_home_status_code(client):
    response = client.get('/')
    assert response.status_code == 200

def test_prediction_text(client):
    response = client.post('/', data={'input': 'Test tweet'})
    assert '* Cette app ne prédit que les Tweets. Veuillez saisir un message de moins de 280 caractères.'.encode('utf-8') not in response.data
    assert '* Veuillez saisir un message.'.encode('utf-8') not in response.data

def test_error_message_for_long_input(client):
    response = client.post('/', data={'input': 'a'*281})
    assert '* Cette app ne prédit que les Tweets. Veuillez saisir un message de moins de 280 caractères.'.encode('utf-8') in response.data

def test_error_message_for_empty_input(client):
    response = client.post('/', data={'input': ''})
    assert '* Veuillez saisir un message.'.encode('utf-8') in response.data

def test_positive_prediction(client):
    response = client.post('/', data={'input': 'Encore une super journée !'})
    assert "Le Tweet est positif.".encode('utf-8') in response.data

def test_negative_prediction(client):
    response = client.post('/', data={'input': 'Encore une horrible journée de merde !'})
    assert "Le Tweet est négatif.".encode('utf-8') in response.data

def test_response_time(client):
    start_time = time.time()
    response = client.post('/', data={'input': 'Test tweet'})
    end_time = time.time()
    assert end_time - start_time < 0.5  # replace 0.5 with your desired threshold in seconds