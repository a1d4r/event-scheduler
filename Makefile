TESTS = tests

VENV ?= .venv
CODE = tests app

.PHONY: venv
venv:
	python3.9 -m venv $(VENV)
	$(VENV)/bin/python -m pip install --upgrade pip
	$(VENV)/bin/python -m pip install poetry
	$(VENV)/bin/poetry install

.PHONY: lint
lint:
	$(VENV)/bin/flake8 --jobs 4 --statistics --show-source $(CODE)
	$(VENV)/bin/pylint --jobs 4 --rcfile=setup.cfg $(CODE)
	$(VENV)/bin/mypy $(CODE)
	$(VENV)/bin/black --skip-string-normalization --check $(CODE)

.PHONY: format
format:
	$(VENV)/bin/isort $(CODE)
	$(VENV)/bin/black --skip-string-normalization $(CODE)
	$(VENV)/bin/autoflake --recursive --in-place --remove-all-unused-imports --exclude=__init__.py $(CODE)
	$(VENV)/bin/unify --in-place --recursive $(CODE)

.PHONY: up
up:
	docker-compose -f docker-compose.yml up -d --build

.PHONY: down
down:
	docker-compose down

.PHONY: test
test:
	docker-compose run --rm app pytest -v tests


.PHONY: ci
ci:	lint test
