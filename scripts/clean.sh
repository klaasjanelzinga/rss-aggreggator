#!/usr/bin/env bash

# --
# removes all build artifacts.

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
project_dir="$(cd "${script_dir}"/.. && pwd )"

rm -rf "$project_dir"/static/build
rm -rf "$project_dir"/build-reports
rm -rf "$project_dir"/.pytest_cache
rm -rf "$project_dir"/.mypy_cache
rm -f "$project_dir"/.coverage

rm -rf "$project_dir"/frontend/node_modules
rm -rf "$project_dir"/frontend/build

exit 0
