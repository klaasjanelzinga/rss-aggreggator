# rss-aggreggator


Master is ![](https://github.com/klaasjanelzinga/rss-aggreggator/workflows/Deploy%20application/badge.svg)


### running the app local

        mkvirtualenv rss-aggreggator
        pip install -r requirements.txt
        pip install -r requirements-dev.txt --upgrade
        scripts/build-docker-image.sh
        docker-compose up --build

Will start 

- react frontend on port 3000
- api python backend on port 8080
- cron python backend on port 8090

Connect to port http://localhost:3000 to see the app. First decypt the secret to connect to a database or follow 
the instructions in `scripts/create-google-appengine-credentials.sh`

If you want to debug a process, stop that process with `docker-compose stop <api|cron|frontend>` and start it locally.

        #   (you may have to sudo rm -rf node_modules && npm i && npm start)
        cd frontend && npm start   # starts frontend
        python api.py   # starts api
        
All processes started with docker-compose are in hot-reload, using watchmedo for python
and npm start for the frontend.

Insert some testdata: `curl localhost:8090/cron/fetch-integration-test-data`

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

        see the Activities.
