.PHONY: init install uninstall wheel format lint clear

NAME = BigkindsParser

SHELL := bash

init_environment = pip install $(pip_user_option) --upgrade pip && \
pip install $(pip_user_option) --upgrade 'build>=0.7' 'setuptools>=61.0,<64.0' 'wheel>=0.37' && \
pip install $(pip_user_option) -r requirements.txt

build_wheel = python3 setup.py bdist_wheel

uninstall_extension = pip uninstall --yes $(NAME)

ifndef production
	init_environment += pre-commit install

	install_extension = pip install $(pip_user_option) -e .
else
	install_extension = $(build_wheel) && \
	pip install $(pip_user_option) --find-links "dist/" $(NAME)
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
	@black --config=pyproject.toml BigKindsParser/ test/
	@isort --settings-file=pyproject.toml BigKindsParser/ test/

lint:
	@flake8 --config=.flake8 BigKindsParser/ test/
	@pylint --rcfile=.pylintrc BigkindsParser/ test/

clear:
	rm -fr BigKindsParser.egg-info/ ; \
	rm -fr build/ dist/ ; \
	rm -fr **/__pycache__ ;
