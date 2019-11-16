script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
project_dir="$(cd "${script_dir}"/.. && pwd )"

set -e
cd $project_dir

docker run -v $project_dir:/usr/src/app rss-aggregator-app scripts/build.sh

export version="develop-`git rev-parse --short HEAD`"
echo "Version: $version"

gcloud auth activate-service-account deployer@rss-aggregator-236707.iam.gserviceaccount.com  --keyfile secrets/deployer.json --project rss-aggregator-236707
gcloud app deploy --version $version --project rss-aggregator-236707 app.yaml
gcloud app deploy --version $version --project rss-aggregator-236707 cron.yaml
