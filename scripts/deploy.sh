script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
project_dir="$(cd "${script_dir}"/.. && pwd )"

cd $project_dir

[[ -z "$VIRTUAL_ENV" ]] && echo "Virtual env not set. Not deploying." && exit 1

if [ "`git status -s`" != "" ]
then
    echo "Git repo is not clean"
    git status
    exit 1
fi 

if [ "`git rev-parse --abbrev-ref HEAD`" != "master" ]
then
    echo "Can only deploy from master"
    exit 1
fi

if [ "`git diff --stat --cached origin/master`" != "" ]
then
    echo "Not all changes are pushed to origin/master"
    git diff --stat --cached origin/master
    exit 1
fi


$project_dir/run-before-commit.sh
[ $? -ne 0 ] && echo "Build / test failed." && exit 1

export version="develop-`git rev-parse --short HEAD`"
echo "Version: $version"

echo gcloud app deploy --version $version --project rss-aggregator-236707 app.yaml
echo gcloud app deploy --version $version --project rss-aggregator-236707 cron.yaml
