#!/bin/sh

# Lancer le backend
gunicorn -b :8001 --reload app:app &
backend_pid=$!

# Lancer le frontend
cd frontend
export FLASK_APP=app_frontend.py
export FLASK_ENV=development
export FLASK_DEBUG=1
export FLASK_RUN_PORT=8000
flask run &
frontend_pid=$!

# Fonction pour terminer les processus en arrière-plan
cleanup() {
    kill $backend_pid
    kill $frontend_pid
}

# Capturer le signal SIGINT et appeler la fonction cleanup
trap cleanup SIGINT

# Attendre que tous les processus en arrière-plan se terminent
wait