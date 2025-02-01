.PHONY: dev format serve test

default: serve

dev:
	python3 app.py --debug

format:
	python3 -m black .

serve:
	python3 app.py

test:
	python3 -m unittest discover -s tests -p "test_*.py"