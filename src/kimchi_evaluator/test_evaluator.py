import src.kimchi_object.object as obj
from src.kimchi_evaluator import eval
from src.kimchi_lexer import Lexer
import src.kimchi_object as obj
import src.kimchi_object.environment as env
from src.kimchi_parser import Parser


def test_array_index_expressions():
    tests = [
        ("[1, 2, 3][0]", 1),
        ("[1, 2, 3][1]", 2),
        ("[1, 2, 3][2]", 3),
        ("let i = 0; [1][i];",1,),
        ( "[1, 2, 3][1 + 1];", 3),
        ("let myArray = [1, 2, 3]; myArray[2];", 3),
        ("let myArray = [1, 2, 3]; myArray[0] + myArray[1] + myArray[2];", 6),
        ("let myArray = [1, 2, 3]; let i = myArray[0]; myArray[i]", 2),
        ("[1, 2, 3][3]", None),
        ("[1, 2, 3][-1]", None)]
    for t in tests:
      evaluated = eval_test(t[0])
      if t[1] is None:
          assert_null_object(evaluated)
      else:
          assert_integer_object(evaluated, t[1])



def test_array_literals():
    input = "[1, 2 * 2, 3 + 3]"
    evaluated = eval_test(input)
    assert isinstance(evaluated, obj.Array)
    assert len(evaluated.elements) == 3
    assert_integer_object(evaluated.elements[0], 1)
    assert_integer_object(evaluated.elements[1], 4)
    assert_integer_object(evaluated.elements[2], 6)


def test_builtin_functions():
    tests = [
        ("len(\"\")", 0),
        ("len(\"four\")", 4),
        ("len(\"hello world\")", 11),
        ("len(1)", "argument to `len` not supported, got INTEGER"),
        ("len(\"one\", \"two\")", "wrong number of arguments. got=2, want=1"),
    ]
    for t in tests:
        evaluated = eval_test(t[0])
        if type(t[1]) is int:
            assert_integer_object(evaluated, t[1])
        else:
            assert isinstance(evaluated, obj.Error)
            assert evaluated.message == t[1]


def test_string_concat():
    input = """
      "Hello" + " " + "World!"
    """
    evaluated = eval_test(input)
    assert isinstance(evaluated, obj.String)
    assert evaluated.value == "Hello World!"


def test_string_literal_expression():
    input = """
      "Hello World!"
    """
    evaluated = eval_test(input)
    assert isinstance(evaluated, obj.String)
    assert evaluated.value == "Hello World!"


def test_closure():
    input = """
    let add = fn(x) {
      fn(y) { x + y };
    };
    let addTwo = add(2);
    addTwo(3);
    """
    evaluated = eval_test(input)
    assert_integer_object(evaluated, 5)


def test_function_application():
    tests = [
        ("let identity = fn(x) { x; }; identity(5);", 5),
        ("let identity = fn(x) { return x; }; identity(5);", 5),
        ("let double = fn(x) { x * 2; }; double(5);", 10),
        ("let add = fn(x, y) { x + y; }; add(5, 5);", 10),
        ("let add = fn(x, y) { x + y; }; add(5 + 5, add(5, 5));", 20),
        # ("fn(x) { x } (5) ", 5),
    ]

    for tt in tests:
        evaluated = eval_test(tt[0])
        assert_integer_object(evaluated, tt[1])


def test_function_object():
    input = "fn(x) { x + 2; };"
    evaluated = eval_test(input)
    assert isinstance(evaluated, obj.Function)
    assert len(evaluated.parameters) == 1
    assert evaluated.parameters[0].value == "x"
    assert str(evaluated.body) == "(x + 2)"


def test_let_statements():
    tests = [
        ("let a = 5; a;", 5),
        ("let a = 5 * 5; a;", 25),
        ("let a = 5; let b = a; b;", 5),
        ("let a = 5; let b = a; let c = a + b + 5; c;", 15),
    ]

    for tt in tests:
        evaluated = eval_test(tt[0])
        assert_integer_object(evaluated, tt[1])


def test_error_handling():
    tests = [
        ("5 + true;", "type mismatch: INTEGER + BOOLEAN"),
        ("5 + true; 5;", "type mismatch: INTEGER + BOOLEAN"),
        ("-true", "unknown operator: -BOOLEAN"),
        ("true + false;", "unknown operator: BOOLEAN + BOOLEAN"),
        ("5; true + false; 5", "unknown operator: BOOLEAN + BOOLEAN"),
        ("if (10 > 1) { true + false; }", "unknown operator: BOOLEAN + BOOLEAN"),
        ("""if (10 > 1) {
          if (10 > 1) {
            return true + false;
          }
        return 1; }""", "unknown operator: BOOLEAN + BOOLEAN"),
        ("foobar", "identifier not found: foobar")
    ]

    for tt in tests:
        evaluated = eval_test(tt[0])
        assert isinstance(evaluated, obj.Error)
        assert evaluated.message == tt[1]


def test_return_statements():
    tests = [
        ("return 10;", 10),
        ("return 10; 9;", 10),
        ("return 2 * 5; 9;", 10),
        ("9; return 2 * 5; 9;", 10),
        ("""
        if (10 > 1) {
            if (10 > 1) {
              return 10;
            }
            return 1
        }""", 10)
    ]

    for tt in tests:
        evaluated = eval_test(tt[0])
        assert_integer_object(evaluated, tt[1])


def test_of_else_expressions():
    tests = [
        ("if (true) { 10 }", 10),
        ("if (false) { 10 }", None),
        ("if (1) { 10 }", 10),
        ("if (1 < 2) { 10 }", 10),
        ("if (1 > 2) { 10 }", None),
        ("if (1 > 2) { 10 } else { 20 }", 20),
        ("if (1 < 2) { 10 } else { 20 }", 10),
    ]

    for tt in tests:
        evaluated = eval_test(tt[0])
        if type(tt[1]) is int:
            assert_integer_object(evaluated, tt[1])
        else:
            assert_null_object(evaluated)


def assert_null_object(value):
    assert isinstance(value, obj.Null)


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
    return eval(program, env.Environment())


def assert_integer_object(obj, expected):
    assert obj.value == expected
    assert obj.type() == "INTEGER"


def assert_boolean_object(obj, expected):
    assert obj.value == expected
    assert obj.type() == "BOOLEAN"

