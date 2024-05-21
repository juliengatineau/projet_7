#!/bin/sh

# Lancer le frontend
export FLASK_APP=app_frontend.py
export FLASK_ENV=development
export FLASK_DEBUG=1
export FLASK_RUN_PORT=8000
flask run &
frontend_pid=$!

# Fonction pour terminer le processus en arrière-plan
cleanup() {
    kill $frontend_pid
}

# Capturer le signal SIGINT et appeler la fonction cleanup
trap cleanup INT

# Attendre que le processus en arrière-plan se termine
wait