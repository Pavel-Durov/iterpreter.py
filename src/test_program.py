import src.kimchi_object as obj
import src.kimchi_object.environment as env
from src.kimchi_evaluator import eval
from src.kimchi_lexer import Lexer
from src.kimchi_parser import Parser


def test_function_calls():
    source = """
    let fibonacci = fn(x) { 
      if (x < 2) {
        return x;
      }
      return fibonacci(x-1) + fibonacci(x-2);
    }; 
    
    let getOne = fn(){
      return 1;
    };
    getOne() + fibonacci(7);
    """
    evaluated = eval_test(source)
    assert isinstance(evaluated, obj.Integer)
    self_like_eval = eval_test(source, True)
    assert evaluated.value == self_like_eval.value == 14


def test_closure():
    input = """
    let add = fn(x) {
      fn(y) { x + y };
    };
    let addTwo = add(2);
    addTwo(3);
    """
    evaluated = eval_test(input)
    assert evaluated.value == 5


def eval_test(str, self_like=False):
    lexer = Lexer(str)
    parser = Parser(lexer)
    program = parser.parse_program()
    if self_like:
        return eval(program, env.SelfLikeObjEnvironment())
    return eval(program, env.Environment())
