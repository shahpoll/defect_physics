PYTHON ?= .venv/bin/python

.PHONY: setup test pdf site all preview figures

setup:
	python3.13 -m venv .venv
	$(PYTHON) -m pip install -r requirements.txt -r requirements-publication.txt

test:
	PYTHONPATH=src $(PYTHON) -m unittest discover -s tests -v
	$(PYTHON) tools/check_reference.py

pdf:
	$(PYTHON) tools/build_publication.py --format pdf

site:
	$(PYTHON) tools/build_publication.py --format site

all: test
	$(PYTHON) tools/build_publication.py --format all

preview: site
	$(PYTHON) -m http.server 8000 --directory build/site

figures:
	$(PYTHON) run_study.py
