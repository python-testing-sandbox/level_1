test:
	python -m pytest
coverage:
	python -m pytest --cov=code --cov-report=xml
check:
	make test
