from src.kimchi_lexer import Lexer
from src.kimchi_parser import Parser
from src.kimchi_evaluator import eval

def test_eval_integer_expression():
    tests = [
      ("5", 5),
      ("10", 10),
    ]
    for tt in tests:
      evaluated = eval_test(tt[0])
      assert_integer_object(evaluated, tt[1])

def test_boolean_expression():
    tests = [
      ("true", True),
      ("false", False),
    ]
    for tt in tests:
      evaluated = eval_test(tt[0])
      assert_boolean_object(evaluated, tt[1])
 
def eval_test(str):
    lexer = Lexer(str)
    parser = Parser(lexer)
    program = parser.parse_program()
    return eval(program)


def assert_integer_object(obj, expected):
    assert obj.value == expected
    assert obj.type() == "INTEGER"

def assert_boolean_object(obj, expected):
    assert obj.value == expected
    assert obj.type() == "BOOLEAN"
