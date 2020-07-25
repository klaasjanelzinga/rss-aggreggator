#!/usr/bin/env bash
# -----
# -v VERSION
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
(cd $script_dir/.. && docker build -t rss-aggregator/api:$VERSION -f api/Dockerfile .)
(cd $script_dir/.. && docker build -t rss-aggregator/cron:$VERSION -f cron/Dockerfile .)
(cd $script_dir/../frontend && docker build -t rss-aggregator/frontend:$VERSION .)

# tag application version -> latest
docker tag rss-aggregator/api:$VERSION rss-aggregator/api:latest
docker tag rss-aggregator/cron:$VERSION rss-aggregator/cron:latest
docker tag rss-aggregator/frontend:$VERSION rss-aggregator/frontend:latest
