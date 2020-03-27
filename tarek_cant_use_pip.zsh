#!/usr/bin/zsh

opt=$1
branch=$2
cd app

if [[ $opt == "run" ]]; then
  if [[ $branch == "dev" ]]; then git checkout dev; fi;
  if [[ $branch == "master" ]]; then git checkout master; fi
  pipenv lock
  pipenv install --dev
  pipenv run flask run
elif [[ $opt == "update" ]]; then
  git checkout master
  git pull
  git checkout dev
  git pull
  pipenv lock
  pipenv install --dev
else
  echo "Invalid command"
  echo "------------------"
  echo "To run the application         --> ./tooling.zsh run [branch-name]"
  echo "To update literally everything --> ./tooling.zsh update"
fi;
cd ..
