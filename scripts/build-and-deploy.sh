#!/usr/bin/env bash

set -e

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

$script_dir/build-docker-images.sh --version BETA
$script_dir/deploy.sh --version BETA $1
