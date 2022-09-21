.PHONY: mock run dev

mock:
	python -m mock.run

freeze:
	pip freeze > requirements.txt

install:
	pip install -r requirements.txt

run:
	flask --app main run --host=0.0.0.0

dev:
	flask --app main --debug run
