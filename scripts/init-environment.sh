#!/usr/bin/env bash

# --
# Initialize build environment (run inside virtualenv of on image)

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
project_dir="$(cd "${script_dir}"/.. && pwd )"

echo "Installing node_modules..."
(cd "$project_dir"/frontend && npm i)
[[ $? -ne 0 ]] && echo "npm i failed" && exit 1

echo "Installing pypy deps..."
(cd "$project_dir" && pip install -r requirements.txt)
[[ $? -ne 0 ]] && echo "pip install failed" && exit 1

exit 0