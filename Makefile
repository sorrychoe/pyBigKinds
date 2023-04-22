.PHONY: init install uninstall wheel format lint clear

NAME = BigkindsParser

SHELL := bash

init_environment = $(python) -m pip install $(pip_user_option) --upgrade pip && \
$(python) -m pip install $(pip_user_option) --upgrade 'build>=0.7' 'setuptools>=61.0,<64.0' 'wheel>=0.37' && \
$(python) -m pip install $(pip_user_option) -r requirements.txt

build_wheel = $(python) setup.py bdist_wheel

uninstall_extension = $(python) -m pip uninstall --yes $(NAME)

ifndef production
	init_environment += git-lfs install && \
	$(python) -m pre_commit install

	install_extension = $(python) -m pip install $(pip_user_option) -e .
else
	install_extension = $(build_wheel) && \
	$(python) -m pip install $(pip_user_option) --find-links "dist/" $(NAME)
endif

init:
	$(init_environment)

install:
	$(install_extension)

uninstall:
	$(uninstall_extension)

wheel:
	$(build_wheel)

format:
	$(python) -m black --config=pyproject.toml BigKindsParser/ setup.py
	$(python) -m isort --settings-file=.isort.cfg BigKindsParser/ setup.py

lint:
	$(python) -m flake8 --config=.flake8 BigKindsParser/ setup.py
	$(python) -W ignore::DeprecationWarning -m pylint --rcfile=.pylintrc BigkindsParser/ setup.py

clear:
	shopt -s globstar ; \
	rm -fr BigKindsParser.egg-info/ ; \
	rm -fr build/ dist/ ; \
	rm -fr **/__pycache__ ;
