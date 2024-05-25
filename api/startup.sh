#!/bin/sh

# Lancer le backend
cd backend 
gunicorn --bind=0.0.0.0:$PORT app:app

# Lancer le frontend
cd ../frontend_dev
export FLASK_APP=app_frontend.py
export FLASK_ENV=development
export FLASK_DEBUG=1
gunicorn --bind=0.0.0.0:$PORT app_frontend:app