cd app
pipenv lock
pipenv install --dev
set FLASK_APP=app.py
pipenv run flask run
