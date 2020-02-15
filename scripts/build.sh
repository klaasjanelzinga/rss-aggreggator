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
black --target-version py37 --check cron.py api.py app/**

echo "Linting ..."
pylint api.py cron.py app/**

echo "Type checking ..."
mypy -p app
mypy api.py
mypy cron.py

echo "Running unit tests ..."
pytest tests --cov . --cov-report=html

echo "coverage report: see file://$project_dir/build-reports/html/index.html"

exit 0
