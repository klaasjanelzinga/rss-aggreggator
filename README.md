# rss-aggreggator

[![Build Status](https://travis-ci.com/klaasjanelzinga/rss-aggreggator.svg?branch=master)](https://travis-ci.com/klaasjanelzinga/rss-aggreggator)


### Required software

travis

        gem install travis -v 1.8.9 --no-rdoc --no-ri`
        travis login --com --auto
     
gcloud

        download sdk: https://cloud.google.com/sdk/docs/
        gcloud init
        gcloud config set project ...

gcloud - travis

        travis encrypt-file client-secret.json --add --com
        
        