#!/usr/bin/env bash

if [ -z "$VIRTUAL_ENV" ]
then
    echo "sourcing venv"
    source venv/bin/activate
    VENV_SOURCED="YES"
fi

echo "Starting app"
ps aux | grep main.py |grep -v gre | awk '{ print $2 }' | xargs kill
if [[ -f ${HOME}/Downloads/test-ds.json ]]
then
    export GOOGLE_APPLICATION_CREDENTIALS=/Users/klaasjanelzinga/Downloads/test-ds.json
else
    export GOOGLE_APPLICATION_CREDENTIALS=`pwd`/test-ds.json
fi

[[ ! -f ${GOOGLE_APPLICATION_CREDENTIALS} ]] && echo "Cannot read in test-ds.json or ~/Downloads/ds.json" && exit 1

python3 main.py &

echo "Running integration..."
pytest integration
result=$?

ps aux | grep main.py |grep -v gre | awk '{ print $2 }' | xargs kill

[ $result != 0 ] && echo "Test failed" && exit 1
exit 0