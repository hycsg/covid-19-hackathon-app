start http://127.0.0.1:5000
cd app
pipenv lock
pipenv install --dev
set FLASK_APP=app.py
pipenv run flask run
pause