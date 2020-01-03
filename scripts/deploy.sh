script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
project_dir="$(cd "${script_dir}"/.. && pwd )"

set -e

export version="develop-`git rev-parse --short HEAD`"
echo "Version: $version"

gcloud app deploy --version $version --project rss-aggregator-236707 app.yaml
gcloud app deploy --version $version --project rss-aggregator-236707 cron.yaml
