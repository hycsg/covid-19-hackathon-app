pip install pipenv
cd app
pipenv lock
pipenv install --dev
set FLASK_APP=app.py
start "" open.bat
pipenv run flask run