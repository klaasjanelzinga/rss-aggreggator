script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
project_dir="$(cd "${script_dir}"/.. && pwd )"

set -e

cd $project_dir && docker build -t rss-aggregator-app .
