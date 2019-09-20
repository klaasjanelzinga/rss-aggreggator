#!/usr/bin/env bash

# --
# runs integration tests

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
project_dir="$(cd "${script_dir}"/.. && pwd )"

cd "$project_dir" || (echo "project_dir not found" && exit 1)

echo "Starting app"
ps aux | grep main.py |grep -v gre | awk '{ print $2 }' | xargs kill
if [[ -f ${HOME}/Downloads/test-ds.json ]]
then
    export GOOGLE_APPLICATION_CREDENTIALS=$HOME/Downloads/test-ds.json
else
    export GOOGLE_APPLICATION_CREDENTIALS=`pwd`/test-ds.json
fi

[[ ! -f ${GOOGLE_APPLICATION_CREDENTIALS} ]] && echo "Cannot read in test-ds.json or ~/Downloads/test-ds.json" && exit 1

python3 main.py &

echo "Running integration..."
pytest integration
result=$?

ps aux | grep main.py |grep -v gre | awk '{ print $2 }' | xargs kill

[ $result != 0 ] && echo "Test failed" && exit 1
exit 0