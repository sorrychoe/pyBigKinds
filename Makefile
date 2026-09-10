.PHONY: init install uninstall wheel release lint format test clear

NAME = pyBigKinds

SHELL := bash
python = python3
pip_user_option = --user

ifeq ($(OS),Windows_NT)
	python := python
endif

ifndef production
	install_extension = pip install $(pip_user_option) -e .
else
	install_extension = $(python) -m build --wheel && \
	pip install $(pip_user_option) --find-links "dist/" $(NAME)
endif

init:
	$(python) -m pip install $(pip_user_option) --upgrade pip && \
	$(python) -m pip install $(pip_user_option) --upgrade 'build>=0.7' 'setuptools>=61.0' 'wheel>=0.37' && \
	$(python) -m pip install $(pip_user_option) -r requirements.txt &&\
	$(python) -m pre_commit install

install:
	$(install_extension)

uninstall:
	pip uninstall --yes $(NAME)

wheel:
	$(python) -m build

lint:
	$(python) -m isort pyBigKinds/ test/

format:
	$(python) -m flake8 --config=setup.cfg pyBigKinds/
	$(python) -m pylint --rcfile=.pylintrc pyBigKinds/

test:
	$(python) -W ignore::FutureWarning -m pytest -v -s

clear:
	shopt -s globstar ; \
	rm -fr pyBigKinds.egg-info/ build/ dist/ ;\
	rm -fr **/__pycache__ **/.pytest_cache ;
