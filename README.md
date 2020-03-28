# Coronavirus hackathon project

Covid in my County (hycsg hackathon project) is a submission to the [covid-global-hackathon](https://covid-global-hackathon.devpost.com). It is an application that enables users to obtain Coronavirus information about their desired United States state and county; additionally showing them CDC resources about the virus and treating/preventing it.

## Running the application

1. Read the instructions listed in this `README.md`

### Windows
```
cd app
pipenv lock
pipenv install --dev
set FLASK_APP=app.py
pipenv run flask run
```

### Linux/MacOS
```sh
$ cd app
$ export FLASK_APP=app.py
$ pipenv lock
$ pipenv install --dev
$ pipenv run flask run
```
