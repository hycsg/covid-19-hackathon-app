#!/usr/bin/env bash

cd app
git checkout master
git pull
export FLASK_APP=app.py
pipenv lock
pipenv install --dev
pipenv run flask run
