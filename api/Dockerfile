FROM rss-aggregator/python-base:latest

COPY api/requirements.txt api/requirements.txt

COPY api /usr/src/app/api
COPY core_lib /usr/src/app/core_lib

RUN cd core_lib && pip install -r requirements.txt
RUN cd api && pip install -r requirements.txt

VOLUME [ "/usr/src/app" ]

CMD ["api/entrypoint.sh"]