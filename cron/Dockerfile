FROM rss-aggregator/python-base:latest

COPY cron /usr/src/app/cron
COPY core_lib /usr/src/app/core_lib

RUN cd core_lib && pip install -r requirements.txt
RUN cd cron && pip install -r requirements.txt

VOLUME [ "/usr/src/app" ]

CMD ["cron/entrypoint.sh"]
