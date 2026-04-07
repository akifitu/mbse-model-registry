PYTHON ?= python3

.PHONY: test catalog

test:
	PYTHONPATH=src $(PYTHON) -m unittest discover -s tests -v

catalog:
	PYTHONPATH=src $(PYTHON) -m mbse_model_registry.cli catalog --data-file data/model_packages.json --export-dir reports
