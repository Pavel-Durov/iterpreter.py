from src.kimchi_lexer import Lexer
from src.kimchi_parser import Parser
from src.kimchi_evaluator import eval

def test_eval_integer_expression():
    tests = [
      ("5", 5),
      ("10", 10),
      ("-5", -5),
      ("-10", -10),
      ("5 + 5 + 5 + 5 - 10", 10),
      ("2 * 2 * 2 * 2 * 2", 32),
      ("-50 + 100 + -50", 0),
      ("5 * 2 + 10", 20),
      ("5 + 2 * 10", 25),
      ("20 + 2 * -10", 0),
      ("50 / 2 * 2 + 10", 60),
      ("2 * (5 + 10)", 30),
      ("3 * 3 * 3 + 10", 37),
      ("3 * (3 * 3) + 10", 37),
      ("(5 + 10 * 2 + 15 / 3) * 2 + -10", 50),
    ]
    for tt in tests:
      evaluated = eval_test(tt[0])
      assert_integer_object(evaluated, tt[1])

def test_boolean_expression():
    tests = [
      ("true", True),
      ("false", False),
      ("1 < 2", True),
      ("1 > 2", False),
      ("1 < 1", False),
      ("1 > 1", False),
      ("1 == 1", True),
      ("1 != 1", False),
      ("1 == 2", False),
      ("1 != 2", True),
      ("true == true", True),
      ("false == false", True),
      ("true == false", False),
      ("true != false", True),
      ("false != true", True),
      ("(1 < 2) == true", True),
      ("(1 < 2) == false", False),
      ("(1 > 2) == true", False),
      ("(1 > 2) == false", True),

    ]
    for tt in tests:
      evaluated = eval_test(tt[0])
      assert_boolean_object(evaluated, tt[1])
 
def test_bang_operator():
    tests = [
      ("!true", False),
      ("!false", True),
      ("!5", False),
      ("!!true", True),
      ("!!false", False),
      ("!!5", True)
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
