
# start proxy on :80 and reverse to backend /api and frontend /
if [ "`uname`" = "Linux" ]
then
  OPTIONAL=--network="host"
  UPSTREAM_HOST="127.0.0.1"
else
  UPSTREAM_HOST="host.docker.internal"
fi

cat default.conf.template | sed "s/__HOST_UPSTREAM__/$UPSTREAM_HOST/g" > default.conf

docker build -t nginx-dev-proxy . 
docker run $OPTIONAL --rm  -p 80:80 --name nginx-dev-proxy nginx-dev-proxy
