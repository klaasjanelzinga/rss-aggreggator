#!/usr/bin/env bash

set -e "test-failed"

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
export GOOGLE_APPLICATION_CREDENTIALS=/Users/klaasjanelzinga/Downloads/ds.json
export FLASK_DEBUG=0
python3 main.py | grep -v INFO &
PID=$!

sleep 10

echo "Running integration..."
python3 integration/local_test.py

ps aux | grep main.py |grep -v gre | awk '{ print $2 }' | xargs kill

sleep 2

echo "Building frontend"
(cd frontend && npm run-script build)

if [ ${VENV_SOURCED} == "YES" ]
then
    deactivate
fi