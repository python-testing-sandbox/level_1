test:
	python -m pytest -p no:warnings --disable-socket
coverage:
	python -m pytest --cov=code --cov-report=xml -p no:warnings --disable-socket
check:
	make test
