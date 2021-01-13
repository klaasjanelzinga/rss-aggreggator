# rss-aggreggator


Main is ![](https://github.com/klaasjanelzinga/rss-aggreggator/workflows/Deploy%20application/badge.svg)

The application is constists of the following modules: 

- api - API for the frontend and for the cron.
- cron - Used to initiate crawls and maintenance.
- core_lib - shared library for cron and api.
- frontend - react site.

### running the app local

        docker-compose up --build

Will start:

- react frontend on port 3000
- api python backend on port 8080
- cron python backend on port 8090

All connections are done over localhost. This way you can run a process locally for debugging purposes.

Connect to port http://localhost:3000 to see the app. First decypt the secret to connect to a database or follow 
the instructions in `scripts/create-google-appengine-credentials.sh`

### Develop the app

If you want to debug a process, stop that process with `docker-compose stop <api|cron|frontend>` and start it locally.

        #   (you may have to sudo rm -rf node_modules && npm i && npm start)
        cd frontend && npm start   # starts frontend
        cd api && python -m api
        
All processes started with docker-compose are in hot-reload, using watchmedo for python
and npm start for the frontend.

Insert some testdata: `curl localhost:8090/cron/fetch-integration-test-data`

        make black    # Run formatting
        make mypy     # Run mypy check
        make pylint   # Run linting
        make flakes   # Run all code checkers

### Running tests

        make tests
        make integration-tests

### Committing

        make before-commit    # runs flakes and the tests, all should pass.

### gcloud

        download sdk: https://cloud.google.com/sdk/docs/
        gcloud init
        gcloud config set project ...

## deploy the app

        see the Activities.
