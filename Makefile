.PHONY: init install uninstall wheel release format test clear

NAME = BigKindsParser

SHELL := bash

python = python3

ifeq ($(OS),Windows_NT)
	python := python
endif

ifndef production
	install_extension = pip install $(pip_user_option) -e .
else
	install_extension = $(python) setup.py bdist_wheel && \
	pip install $(pip_user_option) --find-links "dist/" $(NAME)
endif

init:
	$(python) -m pip install $(pip_user_option) --upgrade pip && \
	$(python) -m pip install $(pip_user_option) --upgrade 'build>=0.7' 'setuptools>=61.0,<64.0' 'wheel>=0.37' && \
	$(python) -m pip install $(pip_user_option) -r requirements.txt \
	pre-commit install

install:
	$(install_extension)

uninstall:
	pip uninstall --yes $(NAME)

wheel:
	$(python) setup.py bdist_wheel

lint:
	$(python) -m isort --settings-file=setup.cfg pyBigKinds/ test/

format:
	$(python) -m flake8 --config=setup.cfg pyBigKinds/ test/
	$(python) -m pylint --rcfile=.pylintrc pyBigKinds/

test:
	$(python) -W ignore::FutureWarning -m pytest -v -s

clear:
	shopt -s globstar ; \
	rm -fr pyBigKinds.egg-info/ build/ dist/ ;\
	rm -fr **/__pycache__ **/.pytest_cache ;
