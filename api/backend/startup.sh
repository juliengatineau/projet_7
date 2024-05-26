#!/bin/bash

# Lancer le backend
source venv/bin/activate
gunicorn --bind=0.0.0.0:$PORT app:app