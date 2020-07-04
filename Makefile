.PHONY: help prepare prepare-mac install test lint run run-venv doc deploy clean

VENV_NAME?=venv
VENV_ACTIVATE=. $(VENV_NAME)/bin/activate

PYTHON_VENV=${VENV_NAME}/bin/python3
PYTHON=/usr/local/bin/python3

PIP=/usr/local/bin/pip3
NPM=npm

SLS=./node_modules/.bin/serverless

.DEFAULT: help
help:
	@echo "make prepare"
	@echo "       prepare development environment, use only once"
	@echo "make prepare-mac"
	@echo "       prepare development environment, use only once (uses Homebrew for install)"
	@echo "make install"
	@echo "       installs local pip & npm dependencies"
	@echo "make test"
	@echo "       run tests"
	@echo "make lint"
	@echo "       run pylint and mypy"
	@echo "make run"
	@echo "       run project using /usr/local/bin/python3"
	@echo "make run-venv"
	@echo "       run project"
	@echo "make doc"
	@echo "       build sphinx documentation"
	@echo "make deploy"
	@echo "       deploys to AWS using Serverless-Framework (SLS)"

prepare:
	sudo apt-get -y install python3.7 python3-pip
	python3 -m pip install virtualenv
	make venv

prepare-mac:
	sudo brew install python3.7 python3-pip npm
	python3 -m pip install virtualenv
	make venv

install:
	${PIP} install -t vendor -r requirements.txt
	${NPM} install

# Requirements are in setup.py, so whenever setup.py is changed, re-run installation of dependencies.
venv: $(VENV_NAME)/bin/activate
$(VENV_NAME)/bin/activate: setup.py
	test -d $(VENV_NAME) || virtualenv -p python3 $(VENV_NAME)
	${PYTHON_VENV} -m pip install -U pip
	${PYTHON_VENV} -m pip install -e .
	touch $(VENV_NAME)/bin/activate


test: venv
	${PYTHON_VENV} -m pytest

lint: venv
	${PYTHON_VENV} -m pylint app.py custom_logging/*.py

run-venv: venv
	${PYTHON_VENV} app.py

run:
	${PYTHON} app.py

doc: venv
	$(VENV_ACTIVATE) && cd docs; make html

deploy:
	${SLS} deploy

clean:
	rm -rf node_modules vendor

clean-all:
	make clean
	rm -rf ./__pycache__ ./custom_logging/__pycache__
	rm -rf ./github_music_status.egg-info
	rm -rf ./.serverless
	rm -rf ./venv
