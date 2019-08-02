#!/usr/bin/env bash

export PYTHONUNBUFFERED=1
export GOOGLE_APPLICATION_CREDENTIALS=/Users/klaasjanelzinga/Downloads/test-ds.json

stop() {
    echo "stopping dev-proxy and python..."
    docker stop nginx-dev-proxy
    ps aux | grep python | grep -v grep | grep main.py | awk '{ print $2 }' | xargs kill
    exit
}

trap 'stop' SIGINT

python3 main.py &
(cd nginx-dev-proxy && ./start-nginx-dev-proxy.sh ) &
( cd frontend && npm start ) &

wait
