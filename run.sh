#!/usr/bin/env bash

pip3 install pipenv
cd app
export FLASK_APP=app.py
pipenv lock
pipenv install --dev
pipenv run flask run &
sleep 2
xdg-open 'http://127.0.0.1:5000'
