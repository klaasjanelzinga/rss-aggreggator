# rss-aggreggator

[![Build Status](https://travis-ci.com/klaasjanelzinga/rss-aggreggator.svg?branch=master)](https://travis-ci.com/klaasjanelzinga/rss-aggreggator)


## Required software

### python 

Upgrade all deps:

        cat requirements.txt | cut -f1 -d= | pip install --upgrade 

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

