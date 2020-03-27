#!/usr/bin/zsh

opt=$1
branch=$2
cd app

case "$opt" in

  run) # pull latest code from selected branch and run flask app
    [ $branch == "dev" ] &&
      git checkout dev;
    [ $branch == "master" ] &&
      git checkout master
    pipenv lock &&
    pipenv install --dev &&
    pipenv run flask run;;

  update) # grab latest code and update all pipenv deps
    git checkout master &&
    git pull &&
    git checkout dev && 
    git pull &&
    pipenv lock &&
    pipenv install --dev;;

  *) # Invalid, print usage
    echo "Invalid command"
    echo "------------------"
    echo "To run the application         --> $0 run [branch-name]"
    echo "To update literally everything --> $0 update";;

esac

cd ..
