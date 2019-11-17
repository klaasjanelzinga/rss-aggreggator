FROM python:3.7-slim

RUN apt-get update && apt-get install -y gcc locales npm procps
RUN echo "nl_NL.UTF-8 UTF-8" >> /etc/locale.gen
RUN locale-gen

EXPOSE 8080
ENV GOOGLE_APPLICATION_CREDENTIALS secrets/google-appengine-credentials.json
ENV PYTHONDONTWRITEBYTECODE 3

WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

VOLUME [ "/usr/src/app" ]

CMD ["python3", "main.py" ]
