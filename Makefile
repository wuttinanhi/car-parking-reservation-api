.PHONY: mock run dev stripe-listen stripe-trigger

mock:
	python -m mock.run

freeze:
	pip freeze > requirements.txt

install:
	pip install -r requirements.txt

run:
	flask --app main:app run --host=0.0.0.0 --port=${PORT}

dev:
	flask --app main:app --debug run --port=${PORT}

stripe-listen:
	stripe listen --forward-to 127.0.0.1:${PORT}/payment/stripe/webhook

stripe-trigger:
	stripe trigger payment_intent.succeeded
