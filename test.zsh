#!/usr/bin/zsh

PROJECT_DIR=${0:a:h}

opt=$1
cd $PROJECT_DIR/app

case "$opt" in

  demo)
    pip3 install pipenv &&
    git checkout master &&
    git pull &&
    pipenv lock &&
    pipenv install --dev &&
    pipenv run flask run
  ;;

  run) # pull latest code from selected branch and run flask app
    [[ $2 == "dev" ]] &&
      git checkout dev;
    [[ $2 == "master" ]] &&
      git checkout master;
    # Update all Pipfile requirements
    export FLASK_APP=app.py
    pipenv lock &&
      pipenv install --dev &&
      pipenv run flask run
  ;;

  update) # grab latest code and update all pipenv deps
    git checkout master &&
      git pull          &&
      git checkout dev  &&
      git pull          &&
      pipenv lock       &&
      pipenv install --dev
  ;;

  *) # Invalid, print usage
    echo "Invalid usage of $0"
    echo "------------------"
    echo "To run the demo                --> $0 demo"
    echo "To run the application         --> $0 run [branch-name]"
    echo "To update literally everything --> $0 update"
    echo "\nNOTE: running installs pipenv and requires python 3.7"
  ;;

esac
