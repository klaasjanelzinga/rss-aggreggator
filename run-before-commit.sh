#!/usr/bin/env bash

VENV_SOURCED="NO"

if [ -z "$VIRTUAL_ENV" ]
then
    echo "sourcing venv"
    source venv/bin/activate
    VENV_SOURCED="YES"
fi

echo "Linting ..."
pylint main.py app/**
[[ $? -ne 0 ]] && echo "Linting failed" && exit 1

echo "Type checking ..."
mypy main.py
[[ $? -ne 0 ]] && echo "Type checking tests failed" && exit 1
echo "MyPy OK"

echo "Running pytests"
pytest tests --cov . --cov-report=html
[[ $? -ne 0 ]] && echo "Pytests tests failed" && exit 1

`pwd`/run-integration-test.sh
[[ $? -ne 0 ]] && echo "Integration tests failed" && exit 1
sleep 1

echo "Building frontend"
(cd frontend && npm run-script build)
[[ $? -ne 0 ]] && echo "Frontend build failed" && exit 1


if [ ${VENV_SOURCED} == "YES" ]
then
    deactivate
fi