.PHONY: init install uninstall wheel format lint clear

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
	pip install $(pip_user_option) --upgrade pip && \
	pip install $(pip_user_option) --upgrade 'build>=0.7' 'setuptools>=61.0,<64.0' 'wheel>=0.37' && \
	pip install $(pip_user_option) -r requirements.txt \
	pre-commit install

install:
	$(install_extension)

uninstall:
	pip uninstall --yes $(NAME)

wheel:
	$(python) setup.py bdist_wheel

format:
	$(python) -m black --config=pyproject.toml BigKindsParser/ test/
	$(python) -m isort --settings-file=pyproject.toml BigKindsParser/ test/

lint:
	$(python) -m flake8 --config=.flake8 BigKindsParser/ test/
	$(python) -m pylint --rcfile=.pylintrc BigKindsParser/ test/

clear:
	rm -fr **/BigKindsParser.egg-info/ ; \
	rm -fr build/ dist/ ; \
	rm -fr **/__pycache__ ;
