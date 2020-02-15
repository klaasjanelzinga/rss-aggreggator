FROM python:3.7-slim

RUN apt-get update && apt-get install -y gcc locales procps
RUN echo "nl_NL.UTF-8 UTF-8" >> /etc/locale.gen
RUN locale-gen

EXPOSE 8080

ENV ENVIRONMENT=PRODUCTION
ENV PYTHONDONTWRITEBYTECODE 3

WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY cron.py /usr/src/app
COPY api.py /usr/src/app
COPY app /usr/src/app/app

VOLUME [ "/usr/src/app" ]

