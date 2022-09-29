.PHONY: mock run dev stripe-listen stripe-trigger

mock:
	python -m mock.run

freeze:
	pip freeze > requirements.txt

install:
	pip install -r requirements.txt

run:
	flask --app main:app run --host=0.0.0.0 --port=5000

dev:
	flask --app main:app --debug run --port=5000

stripe-listen:
	stripe listen --forward-to 127.0.0.1:5000/payment/stripe/webhook

stripe-trigger:
	stripe trigger payment_intent.succeeded
