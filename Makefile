black:
	black core_lib/tests core_lib/core_lib 
	black api/api api/tests 
	black cron/cron cron/tests

black-check:
	black --check core_lib/tests core_lib/core_lib 
	black --check api/api api/tests 
	black --check cron/cron cron/tests

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
	(cd core_lib && pytest --cov core_lib --cov-report=html tests)

dev-requirements:
	pip install -r requirements.txt
	(cd core_lib && pip install -r requirements.txt)
	(cd api && pip install -r requirements.txt)
	(cd cron && pip install -r requirements.txt)

build-docker-images:
	scripts/build-docker-images.sh

integration-tests:
	(cd integration && docker-compose up --exit-code-from integration_test integration_test)

integration-tests-down:
	(cd integration && docker-compose down)


up: 
	docker-compose up --build

before-commit: flakes tests build-docker-images integration-tests

