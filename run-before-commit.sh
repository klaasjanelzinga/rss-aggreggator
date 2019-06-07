#!/usr/bin/env bash

VENV_SOURCED="NO"

if [ -z "$VIRTUAL_ENV" ]
then
    echo "sourcing venv"
    source venv/bin/activate
    VENV_SOURCED="YES"
fi

echo "Running pytests"
pytest tests --cov . --cov-report=html

echo "Starting app"
ps aux | grep main.py |grep -v gre | awk '{ print $2 }' | xargs kill
export GOOGLE_APPLICATION_CREDENTIALS=/Users/klaasjanelzinga/Downloads/ds.json
python3 main.py | grep -v INFO &

sleep 10

echo "Running integration..."
python3 integration/local_test.py
result=$?

ps aux | grep main.py |grep -v gre | awk '{ print $2 }' | xargs kill

[ $result != 0 ] && echo "Test failed" && exit 1

sleep 2

echo "Building frontend"
(cd frontend && npm run-script build)

if [ ${VENV_SOURCED} == "YES" ]
then
    deactivate
fi