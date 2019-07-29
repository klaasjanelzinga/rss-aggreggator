
# start proxy on :80 and reverse to backend /api and frontend /

docker build -t snapshot . && docker run -p 80:80 snapshot