PYTHONPATH=${PWD}:${PWD}/src/:${PWD}/.pypy/
VERSION := 0.4.0
PYPY_VERSION_ARTIFACT := pypy2.7-v7.3.9-src
BENCH_BIN=./bin/0.4.0/0.4.0_0ef9af68f13bc45c233617e2d2954df62ebfdd78_main-jit-c

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
	./scripts/translate_and_store.sh ${VERSION} ./src/main.py
	
run-jit-logs:
	PYPYLOG=jit-log-opt:${BENCH_BIN}.logfile ${BENCH_BIN} ./programs/fibo.ki self-like
	PYPYLOG=jit-log-opt:${BENCH_BIN}.logfile ${BENCH_BIN} ./programs/fibo.ki

hyperfine:
	hyperfine './bin/0.4.0/0.4.0_0ef9af68f13bc45c233617e2d2954df62ebfdd78_main-jit-c ./programs/bench.ki self-like' './bin/0.4.0/0.4.0_0ef9af68f13bc45c233617e2d2954df62ebfdd78_main-jit-c ./programs/bench.ki'

git-lfs:
	git lfs track ./bin/**/*-c
