
# start proxy on :80 and reverse to backend /api and frontend /

docker build -t nginx-dev-proxy . && docker run --rm  -p 80:80 --name nginx-dev-proxy nginx-dev-proxy