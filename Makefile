.PHONY: default

install:
	pipenv install --skip-lock

build:
	python setup.py bdist_wheel

install_package:
	pip install dist/redditkeys-0.1.0-py2.py3-none-any.whl
