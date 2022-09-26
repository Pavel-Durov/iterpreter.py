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
	PYPYLOG=jit-log-opt:bin/0.4.0/0.4.0_990f4184c71810fb7aaa3478b0e403a953f4324b_main-jit-self-like-loops-c.logfile bin/0.4.0/0.4.0_990f4184c71810fb7aaa3478b0e403a953f4324b_main-jit-c ./programs/loops.ki self-like
	PYPYLOG=jit-log-opt:bin/0.4.0/0.4.0_990f4184c71810fb7aaa3478b0e403a953f4324b_main-jit-loops-c.logfile bin/0.4.0/0.4.0_990f4184c71810fb7aaa3478b0e403a953f4324b_main-jit-c ./programs/loops.ki

hyperfine-loops-recursive-jit:
	hyperfine -m 50 -M 50 './bin/0.4.0/0.4.0_990f4184c71810fb7aaa3478b0e403a953f4324b_main-jit-c ./programs/loops_recursive.ki self-like' './bin/0.4.0/0.4.0_990f4184c71810fb7aaa3478b0e403a953f4324b_main-jit-c ./programs/loops_recursive.ki'

hyperfine-loops-jit:
	hyperfine -m 100 -M 100 './bin/0.4.0/0.4.0_990f4184c71810fb7aaa3478b0e403a953f4324b_main-jit-c ./programs/loops.ki self-like' './bin/0.4.0/0.4.0_990f4184c71810fb7aaa3478b0e403a953f4324b_main-jit-c ./programs/loops.ki'

hyperfine-no-jit:
	hyperfine  -m 50 -M 50  './bin/0.4.0/0.4.0_990f4184c71810fb7aaa3478b0e403a953f4324b_main-c ./programs/loops.ki self-like' './bin/0.4.0/0.4.0_990f4184c71810fb7aaa3478b0e403a953f4324b_main-c ./programs/loops.ki'


git-lfs:
	git lfs track ./bin/**/*-c
