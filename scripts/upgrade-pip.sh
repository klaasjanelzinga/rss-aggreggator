#!/usr/bin/env bash

# --
# runs integration tests

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
project_dir="$(cd "${script_dir}"/.. && pwd )"

cd "$project_dir" || (echo "project_dir not found" && exit 1)

cat requirements.txt | cut -f1 -d= | xargs pip install --upgrade
pip freeze > requirements.txt

echo ""
echo ""
echo ""
echo "- environment upgraded"
echo "- requirements.txt editted."
echo ""
exit 0
