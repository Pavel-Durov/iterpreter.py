PYTHONPATH=${PWD}:${PWD}/src/:${PWD}/.pypy/
VERSION := 0.0.2
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
	PYTHONPATH=$(PYTHONPATH) python ./src/awk_repl.py

translate:
	PYTHONPATH=$(PYTHONPATH) python .pypy/rpython/translator/goal/translate.py ${PWD}/src/awk_main.py

get-pypy:
	wget https://downloads.python.org/pypy/$(PYPY_VERSION_ARTIFACT).tar.bz2
	tar -xvf $(PYPY_VERSION_ARTIFACT).tar.bz2 && mv ./$(PYPY_VERSION_ARTIFACT) .pypy && rm $(PYPY_VERSION_ARTIFACT).tar.bz2
