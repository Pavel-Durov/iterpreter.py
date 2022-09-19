[![Test](https://github.com/Pavel-Durov/iterpreter.rpy/actions/workflows/test.yml/badge.svg)](https://github.com/Pavel-Durov/iterpreter.rpy/actions/workflows/test.yml)
[![RPython Translate](https://github.com/Pavel-Durov/iterpreter.rpy/actions/workflows/rpython.yml/badge.svg)](https://github.com/Pavel-Durov/iterpreter.rpy/actions/workflows/rpython.yml)


## iterpreter.rpy

Interpreter written in RPython (WIP)

### Getting started
```shell
$ make init-env # created conda environemnt
$ direnv allow # setup local shell session
```

### Run Test
```shell
$ make test
```

### Run Repl
```shell
$ make repl
```

## Pypy Translate
```shell
$ make get-pypy # downloads and extracts pypy source code
$ make translate # translate ./src RPython to c
```