#!/usr/bin/env bash

pip3 install pipenv
cd app
export FLASK_APP=app.py
pipenv lock
pipenv install --dev
xdg-open 'http://127.0.0.1:5000'
pipenv run flask run