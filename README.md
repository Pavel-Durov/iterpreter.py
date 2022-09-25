[![Test](https://github.com/Pavel-Durov/iterpreter.rpy/actions/workflows/test.yml/badge.svg)](https://github.com/Pavel-Durov/iterpreter.rpy/actions/workflows/test.yml)
[![RPython Translate](https://github.com/Pavel-Durov/iterpreter.rpy/actions/workflows/rpython.yml/badge.svg)](https://github.com/Pavel-Durov/iterpreter.rpy/actions/workflows/rpython.yml)


## kimchi.py

Interpreter called Kimchi, Inspired by a book [Writing An Interpreter In Go](https://interpreterbook.com/) but was writen in RPython.

VM:
+ SELF-Like scope environment optimization

Kimchi Support:
+ Mathematical Expressions - `2 + 4 / (2- 1)`
+ Variable Bindings - `let a = 5` 
+ Conditional Expressions - `(fn(x) { if (x == 1) {return x;} return 9; };)(1)`
+ Return statements - `let getO = fn() { return 1; }`
+ Functions & Function application & closuers - `(fn(x) { return fn(y) { return x + y; }; };)(1)(2);`
+ Higher-Order functions

Supported Data Types:

+ Integers - `1`
+ Booleans - `true, false`
+ Strings - `"Helllo"`
+ Arrays - `[1, false, "yo"]`
+ Hashes - `{ "kimchi": true, 2022: false }`



## Running kimchi sample programs:
```shell
$ python ./src/main.py ${PWD}/programs/fibo.ki          
result: 
13

$ python ./src/main.py ${PWD}/programs/helloWorld.ki 
Hello World
```

## Running kimchi Repl:
```shell
$ python ./src/repl.py       
> let a = {"a": 1, true: 2, 3:4};
> a["a"] 
1
> 22 + 22 == 44
True
```

# Local development
## Setup
```shell
$ make init-env # created conda environemnt
$ direnv allow # setup local shell session
```

### Test
```shell
$ make test
```


## Pypy Translate
```shell
$ make get-pypy # downloads and extracts pypy source code
$ make translate # translate ./src RPython to c
```