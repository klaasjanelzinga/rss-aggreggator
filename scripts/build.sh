#!/usr/bin/env bash

# --
# builds

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
project_dir="$(cd "${script_dir}"/.. && pwd )"

cd "$project_dir" || (echo "project_dir not found" && exit 1)

echo "Checking for pip upgrades ..."
pip list --outdated

echo "Code formatting ..."
black --target-version py37 --check main.py app/**
[[ $? -ne 0 ]] && echo "Code formatting failed" && exit 1

echo "Linting ..."
pylint main.py app/**
[[ $? -ne 0 ]] && echo "Linting failed" && exit 1

echo "Type checking ..."
mypy main.py
[[ $? -ne 0 ]] && echo "Type checking tests failed" && exit 1

pytest tests --cov . --cov-report=html
[[ $? -ne 0 ]] && echo "Pytests tests failed" && exit 1

echo "Building frontend"
cd "$project_dir"/frontend || (echo "frontend_dir not found" && exit 1)

npm run-script build
[[ $? -ne 0 ]] && echo "Frontend build failed" && exit 1
cat build/index.html | sed 's/main\..*\.chunk\.css/main.css/'  > build/index2.html
[[ $? -ne 0 ]] && echo "Frontend build failed" && exit 1

mv build/index2.html build/index.html
mv build/static/css/main.*.chunk.css build/static/css/main.css

rm -rf ../static/build && mv build ../static
[[ $? -ne 0 ]] && echo "Frontend build failed" && exit 1

echo "coverage report: see file://$project_dir/build-reports/html/index.html"
exit 0
