#!/usr/bin/zsh

PROJECT_DIR=${0:a:h}

opt=$1
cd $PROJECT_DIR/app

case "$opt" in

  run) # pull latest code from selected branch and run flask app
    branch=$2;
    [[ $branch == "dev" ]]     \
      && git checkout dev;
    [[ $branch == "master" ]]  \
      && git checkout master;
    # Update all Pipfile requirements
    pipenv lock \
      && pipenv install --dev \
      && pipenv run flask run
  ;;

  update) # grab latest code and update all pipenv deps
    git checkout master    \
      && git pull          \
      && git checkout dev  \
      && git pull          \
      && pipenv lock       \
      && pipenv install --dev
  ;;

  *) # Invalid, print usage
    echo "Invalid command"
    echo "------------------"
    echo "To run the application         --> $0 run [branch-name]"
    echo "To update literally everything --> $0 update";;

esac
