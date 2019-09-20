#!/usr/bin/env bash

export PYTHONUNBUFFERED=1
export GOOGLE_APPLICATION_CREDENTIALS=$HOME/Downloads/test-ds.json

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
project_dir="$(cd "${script_dir}"/.. && pwd )"

cd "$project_dir" || (echo "project_dir not found" && exit 1)


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
