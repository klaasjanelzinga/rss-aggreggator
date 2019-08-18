# rss-aggreggator

[![Build Status](https://travis-ci.com/klaasjanelzinga/rss-aggreggator.svg?branch=master)](https://travis-ci.com/klaasjanelzinga/rss-aggreggator)


### running the app local

        ./start-all.sh

Will start 

- a docker nginx frontend in docker on port 80
- react frontend on port 3000
- python backend on port 8080

Connect to port 80 to see the app. You will need a gcloud database with priviliges.

## Required software

- python3.7
- docker


### python 

Upgrade all deps:

        cat requirements.txt | cut -f1 -d= | xargs pip install --upgrade 

### travis

        gem install travis -v 1.8.9 --no-rdoc --no-ri`
        travis login --com --auto
       
     
### gcloud

        download sdk: https://cloud.google.com/sdk/docs/
        gcloud init
        gcloud config set project ...

### gcloud - travis

        travis encrypt-file secrets.tar --add --com
        # contains travis-deployer.json and test-ds.json
        
    
### run coverage pytest -> html

        (venv) $ pytest --cov . --cov-report=html 

