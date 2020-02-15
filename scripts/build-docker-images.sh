#!/usr/bin/env bash

set -e

VERSION="BETA"

while [[ $# -gt 0 ]]
do
  case "$1" in
    "--version")
      VERSION="$2"
      shift
      ;;
    *)
      echo "$1 $0 -v|--version" && exit 1
      ;;
  esac
  shift
done

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

echo "Building app container"
(cd $script_dir/.. && docker build -t rss-aggregator/application:$VERSION .)
(cd $script_dir/.. && docker build -t rss-aggregator/dev:$VERSION -f Dockerfile-dev .)
(cd $script_dir/../frontend && docker build -t rss-aggregator/frontend:$VERSION .)

docker tag rss-aggregator/application:$VERSION rss-aggregator/api:$VERSION
docker tag rss-aggregator/application:$VERSION rss-aggregator/cron:$VERSION

# tag application version -> latest
docker tag rss-aggregator/application:$VERSION rss-aggregator/application:latest
docker tag rss-aggregator/frontend:$VERSION rss-aggregator/frontend:latest
docker tag rss-aggregator/dev:$VERSION rss-aggregator/dev:latest

