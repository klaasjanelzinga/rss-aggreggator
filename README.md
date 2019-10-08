# rss-aggreggator

[![Build Status](https://travis-ci.com/klaasjanelzinga/rss-aggreggator.svg?branch=master)](https://travis-ci.com/klaasjanelzinga/rss-aggreggator)


### running the app local

        scripts/start-all.sh

Will start 

- a docker nginx frontend in docker on port 80
- react frontend on port 3000
- python backend on port 8080

Connect to port 80 to see the app. You will need a gcloud database with priviliges, the authorization file must be
named `test-ds.json` in `$HOME/Downloads`.

## Required software

- python3.7
- docker
- npm / node

## Building the app

        scripts/init-environment.sh - initializes pip and npm, run inside virtualenv!
        scripts/build.sh - builds, unittest.
        scripts/integration-test.sh - runs app integration test.
        scripts/clean.sh - removes all build artifacts.
        scripts/upgrade-pip.sh - upgrade pip dependencies.

        ./run-before-commit.sh - cleans, builds and tests the app.

### run coverage pytest -> html

        (venv) $ pytest --cov . --cov-report=html tests


### travis

        gem install travis -v 1.8.9 --no-rdoc --no-ri`
        travis login --com --auto
       
     
### gcloud

        download sdk: https://cloud.google.com/sdk/docs/
        gcloud init
        gcloud config set project ...

## deploy the app

        scripts/deploy.sh

You should have a clean repo and be on master.