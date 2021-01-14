black:
	black core_lib/core_lib
	black api/api
	black cron/cron
	black unittests/tests

black-check:
	black --check core_lib/core_lib
	black --check api/api
	black --check cron/cron
	black --check unittests/tests

pylint:
	pylint core_lib/core_lib api/api cron/cron

mypy:
	(cd core_lib && mypy --config-file ../mypy.ini -p core_lib)
	(cd api && mypy --config-file ../mypy.ini -p api)
	(cd cron && mypy --config-file ../mypy.ini  -p cron)

outdated:
	pip list --outdated

flakes: black pylint mypy outdated flake8

flakes-check: black-check pylint mypy outdated flake8

flake8:
	flake8 core_lib/core_lib

tests:
	(cd unittests && export unit_tests=1 && pytest --cov core_lib --cov-report=html tests)

requirements:
	pip install -r requirements.txt
	(cd core_lib && pip install -r requirements.txt)
	(cd api && pip install -r requirements.txt)
	(cd cron && pip install -r requirements.txt)
	(cd unittests && pip install -r requirements.txt)

update-requirements:
	pip-compile requirements.in
	(cd core_lib && pip-compile requirements.in)
	(cd api && pip-compile requirements.in)
	(cd cron && pip-compile requirements.in)
	(cd unittests && pip-compile requirements.in)

build-docker-images:
	scripts/build-docker-images.sh

up:
	docker-compose up --build

before-commit: flakes tests build-docker-images

clean-data:
	curl localhost:8090/cron/cleanup


fetch-integration-test-data:
	curl localhost:8090/cron/fetch-integration-test-data

fetch-data:
	curl localhost:8090/cron/fetch-data

fetch-events-xml:
	curl localhost:8080/events.xml

