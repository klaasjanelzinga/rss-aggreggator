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

`pwd`/run-integration-test.sh
[[ $? -ne 0 ]] && echo "Integration tests failed" && exit 1
sleep 1

echo "Building frontend"
(cd frontend && npm run-script build)

pylint main.py app/**

if [ ${VENV_SOURCED} == "YES" ]
then
    deactivate
fi