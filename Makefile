PYTHON := .venv/bin/python

.PHONY: setup collect build validate test serve manual all
setup:
	python3 -m venv .venv
	$(PYTHON) -m pip install -r requirements.txt
collect:
	$(PYTHON) src/collect.py
build:
	$(PYTHON) src/build.py
	$(PYTHON) src/prepare_web.py
validate:
	$(PYTHON) src/validate.py
test:
	$(PYTHON) -m pytest -q
serve:
	$(PYTHON) src/server.py
manual:
	$(PYTHON) src/make_manual.py
all: collect build validate test
