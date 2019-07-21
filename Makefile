.PHONY: default

default: test

install:
	pipenv install --skip-lock

test:
	python ./src/redditkeys/cli.py announcements --last 100

build_package:
	python setup.py bdist_wheel

install_package:
	pip install dist/redditkeys-0.1.0-py2.py3-none-any.whl
