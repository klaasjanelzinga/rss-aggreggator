#!/usr/bin/env bash
set -e
script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

$script_dir/scripts/build-docker-image.sh
docker run -v $script_dir:/usr/src/app rss-aggregator-app scripts/build.sh

set +e
docker-compose -f integration-test-dc.yml up --exit-code-from integration_test integration_test
result=$?
docker-compose -f integration-test-dc.yml down
[ $result -ne 0 ] && docker-compose -f integration-test-dc.yml logs && exit 1

exit 0
