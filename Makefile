PYTHONPATH=${PWD}:${PWD}/src/:${PWD}/.pypy/

init-env: 
	conda env create -f environment.yml
	curl -sSL https://install.python-poetry.org | python3 -
	conda init zsh && conda activate interpreter-py
	# poetry install
	conda install -n interpreter-py ./requirements.txt

clean-env: 
	conda deactivate
	conda env remove -n interpreter-py

lint-fix:
	black ./src/**/*.py

clone-pypy:
	hg clone https://foss.heptapod.net/pypy/pypy .pypy	
run:
	PYTHONPATH=$(PYTHONPATH) python ./src/main.py
test: 
	pytest ./src

translate-some:
	python ./.pypy/rpython/translator/goal/translate.py /Users/kimchi/git-repos/side-projects/iterpreter.rpy/src/lexer/lexer.py


get-pypy:
	wget https://downloads.python.org/pypy/pypy3.9-v7.3.9-src.tar.bz2
	tar -xvf pypy3.9-v7.3.9-src.tar.bz2 .pypy-src
	wget https://downloads.python.org/pypy/pypy3.9-v7.3.9-osx64.tar.bz2
	tar -xvf pypy3.9-v7.3.9-osx64.tar.bz2 .pypy-bin

poetry-tree:
	poetry show --tree