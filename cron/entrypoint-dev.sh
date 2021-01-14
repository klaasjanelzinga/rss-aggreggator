#!/usr/bin/env bash
# Meant to run in a docker container for dev purposes

pip install -r requirements.txt
(cd cron && pip install -r requirements.txt)
(cd core_lib && pip install -r requirements.txt)

cd cron
watchmedo auto-restart --recursive --pattern=*.py --directory=.. -- python -m cron
