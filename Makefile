freeze:
	pip freeze > requirements.txt

install:
	pip install -r requirements.txt

run:
	flask --app main run 

dev:
	flask --app main --debug run 
