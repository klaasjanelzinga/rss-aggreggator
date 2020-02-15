#!/usr/bin/env bash
# Meant to run in a docker container for dev purposes

watchmedo auto-restart --recursive --pattern=*.py --directory=. -- python3 $1
