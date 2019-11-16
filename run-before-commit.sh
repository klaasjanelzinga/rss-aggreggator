#!/usr/bin/env bash
set -e
script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

$script_dir/scripts/build-docker-image.sh
docker run -v $script_dir:/usr/src/app rss-aggregator-app scripts/build.sh

exit 0
