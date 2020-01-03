#!/usr/bin/env bash

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Builds application.
#
# artifacts:
# build-report/
# - coverage reports etc.
# static/
# - optimized build of frontend
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
set -e

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
project_dir="$(cd "${script_dir}"/.. && pwd )"

cd "$project_dir" || (echo "project_dir not found" && exit 1)

echo "Checking for pip upgrades ..."
pip list --outdated

echo "Code formatting ..."
black --target-version py37 --check main.py app/**

echo "Linting ..."
pylint main.py app/**

echo "Type checking ..."
mypy main.py

echo "Running unit tests ..."
pytest tests --cov . --cov-report=html

echo "Building frontend"
cd "$project_dir"/frontend

npm i
npm run-script build
cat build/index.html | sed 's/main\..*\.chunk\.css/main.css/'  > build/index2.html

mv build/index2.html build/index.html
mv build/static/css/main.*.chunk.css build/static/css/main.css

rm -rf ../static/build && mv build ../static

echo "coverage report: see file://$project_dir/build-reports/html/index.html"

exit 0
