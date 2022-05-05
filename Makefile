format:
	pipenv run isort app tests
	pipenv run black app tests

test:
	pipenv run python -m pytest tests