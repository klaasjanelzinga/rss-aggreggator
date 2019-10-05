#!/usr/bin/env bash

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

"$script_dir"/scripts/init-environment.sh
[[ $? -ne 0 ]] && echo "init failed" && exit 1

"$script_dir"/scripts/build.sh
[[ $? -ne 0 ]] && echo "build failed" && exit 1

"$script_dir"/scripts/integration-test.sh
[[ $? -ne 0 ]] && echo "failed" && exit 1

exit 0
