# rss-aggreggator

[![Build Status](https://travis-ci.com/klaasjanelzinga/rss-aggreggator.svg?branch=master)](https://travis-ci.com/klaasjanelzinga/rss-aggreggator)


### running the app local

        scripts/build-docker-image.sh
        docker-compose up --build

Will start 

- a docker nginx frontend in docker on port 80
- react frontend on port 3000
- python backend on port 8080

Connect to port 80 to see the app. First decypt the secret to connect to a database or follow 
the instructions in `scripts/create-google-appengine-credentials.sh`

## Required software

- docker

## Building the app

        scripts/build.sh - builds, unittest.
        scripts/clean.sh - removes all build artifacts.
        scripts/upgrade-pip.sh - upgrade pip dependencies.

        ./run-before-commit.sh - cleans, builds and tests the app.

### run coverage pytest -> html

        (venv) $ pytest --cov . --cov-report=html tests

     
### gcloud

        download sdk: https://cloud.google.com/sdk/docs/
        gcloud init
        gcloud config set project ...

## deploy the app

        scripts/deploy.sh

You should have a clean repo and be on master.
