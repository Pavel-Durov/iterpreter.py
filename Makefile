PYTHONPATH=${PWD}:${PWD}/src/

init: 
	python3 -m venv .venv

lint-fix:
	black ./src/**/*.py

test: 
	pytest ./src