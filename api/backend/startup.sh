#!/bin/sh

# Lancer le backend
gunicorn --bind=0.0.0.0:$PORT app:app