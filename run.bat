pip install pipenv
cd app
pipenv lock
pipenv install --dev
set FLASK_APP=app.py
start http://127.0.0.1:5000
pipenv run flask run