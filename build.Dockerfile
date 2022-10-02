FROM python:2.7.18

WORKDIR /app

ENV PYPY_VERSION_ARTIFACT=pypy2.7-v7.3.9-src
RUN wget https://downloads.python.org/pypy/${PYPY_VERSION_ARTIFACT}.tar.bz2
RUN tar -xvf ${PYPY_VERSION_ARTIFACT}.tar.bz2 && mv ./${PYPY_VERSION_ARTIFACT} .pypy && rm ${PYPY_VERSION_ARTIFACT}.tar.bz2

COPY . .
# RUN pip install -r ./requirments.txt
ENV PYTHONPATH=/app:/app/src/:/app/.pypy/

RUN ./scripts/translate_and_store.sh build-version ./src/main.py jit