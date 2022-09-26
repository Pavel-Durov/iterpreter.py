PYTHONPATH=${PWD}:${PWD}/src/:${PWD}/.pypy/
VERSION := 0.4.0
PYPY_VERSION_ARTIFACT := pypy2.7-v7.3.9-src

.PHONY: test src

version:
	@echo $(VERSION)

run:
	PYTHONPATH=$(PYTHONPATH) python ./src/main.py

test: 
	pytest ./src

init-env: 
	conda env create -f environment.yml
	conda init zsh && conda activate interpreter-py
	conda install pytest

clean-env: 
	conda deactivate
	conda env remove -n interpreter-py

repl:
	PYTHONPATH=$(PYTHONPATH) python ./src/repl.py

get-pypy:
	wget https://downloads.python.org/pypy/$(PYPY_VERSION_ARTIFACT).tar.bz2
	tar -xvf $(PYPY_VERSION_ARTIFACT).tar.bz2 && mv ./$(PYPY_VERSION_ARTIFACT) .pypy && rm $(PYPY_VERSION_ARTIFACT).tar.bz2

pypy-translate:
	./scripts/translate_and_store.sh ${VERSION} ./src/main.py jit
	# ./scripts/translate_and_store.sh ${VERSION} ./src/main.py
	
run-jit-logs:
	PYPYLOG=jit-log-opt:./bin/0.3.0/0.3.0_5525e8cc7f90b423da45f17f34996553f874e8ab_main-jit_fibo_-c.logfile ./bin/0.3.0/0.3.0_5525e8cc7f90b423da45f17f34996553f874e8ab_main-jit-c ./programs/fibo.ki self-like
	PYPYLOG=jit-log-opt:./bin/0.3.0/0.3.0_5525e8cc7f90b423da45f17f34996553f874e8ab_main-self-like-jit_fibo_-c.logfile ./bin/0.3.0/0.3.0_5525e8cc7f90b423da45f17f34996553f874e8ab_main-jit-c ./programs/fibo.ki

hyperfine:
	hyperfine './bin/0.3.0/0.3.0_5525e8cc7f90b423da45f17f34996553f874e8ab_main-jit-c ./programs/bench.ki self-like' './bin/0.3.0/0.3.0_5525e8cc7f90b423da45f17f34996553f874e8ab_main-jit-c ./programs/bench.ki'

git-lfs:
	git lfs track ./bin/**/*
