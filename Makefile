PYTHONPATH=${PWD}:${PWD}/src/:${PWD}/.pypy/

init-env: 
	conda env create -f environment.yml
	conda init zsh && conda activate interpreter-py
	pip install -r ./requirements.txt

clean-env: 
	conda deactivate
	conda env remove -n interpreter-py

lint-fix:
	black ./src/**/*.py

clone-pypy:
	hg clone https://foss.heptapod.net/pypy/pypy .pypy	

repl:
	PYTHONPATH=$(PYTHONPATH) python ./src/repl.py

run:
	PYTHONPATH=$(PYTHONPATH) python ./src/main.py

test: 
	# pytest ./src
	# TODO: fix local machine error
	~/opt/anaconda3/envs/interpreter-py/bin/py.test ./src
