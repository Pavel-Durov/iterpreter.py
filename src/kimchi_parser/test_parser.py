from src.kimchi_ast.ast import (
    Boolean,
    CallExpression,
    ExpressionStatement,
    FunctionLiteral,
    HashLiteral,
    Identifier,
    IfExpression,
    InfixExpression,
    IntegerLiteral,
    LetStatement,
    ReturnStatement,
    Expression,
    IndexExpression,
    StringLiteral,
)

from src.kimchi_lexer import Lexer
from src.kimchi_parser import Parser


def test_parsing_hash_literal_with_expressions():
    input = "{\"one\": 0 + 1, \"two\": 10 - 8, \"three\": 15 / 5}"
    p = Parser(Lexer(input))
    prog = p.parse_program()
    assert_no_parser_errors(p.errors)
    assert isinstance(prog.statements[0], ExpressionStatement)
    assert isinstance(prog.statements[0].expression, HashLiteral)
    assert len(prog.statements[0].expression.pairs) == 3
    tests = {
        "one": lambda exp: assert_infix_expression(exp, 0, "+", 1),
        "two": lambda exp: assert_infix_expression(exp, 10, "-", 8),
        "three": lambda exp: assert_infix_expression(exp, 15, "/", 5),
    }
    for key in prog.statements[0].expression.pairs:
        tests[str(key)](prog.statements[0].expression.pairs[key])


def test_parsing_empty_hash_literal():
    input = "{}"
    p = Parser(Lexer(input))
    prog = p.parse_program()
    assert_no_parser_errors(p.errors)
    assert isinstance(prog.statements[0], ExpressionStatement)
    assert isinstance(prog.statements[0].expression, HashLiteral)
    assert len(prog.statements[0].expression.pairs) == 0


def test_parsing_hash_literal_string_keys():
    input = "{\"one\": 1, \"two\": 2, \"three\": 3}"
    p = Parser(Lexer(input))
    prog = p.parse_program()
    assert_no_parser_errors(p.errors)
    assert isinstance(prog.statements[0], ExpressionStatement)
    assert isinstance(prog.statements[0].expression, HashLiteral)
    assert len(prog.statements[0].expression.pairs) == 3
    expected = {"one": 1, "two": 2, "three": 3}
    exp = prog.statements[0].expression
    for key in exp.pairs:
        assert isinstance(key, StringLiteral)
        assert key.value in expected
        assert_integer_literal(exp.pairs[key], expected[key.value])


def test_parsing_index_expression():
    p = Parser(Lexer("myArray[1 + 1];"))
    prog = p.parse_program()
    assert_no_parser_errors(p.errors)
    assert isinstance(prog.statements[0], ExpressionStatement)
    assert isinstance(prog.statements[0].expression, IndexExpression)
    assert_infix_expression(prog.statements[0].expression.index, 1, "+", 1)


def test_parsing_array_literals():
    input = "[1,2*2,3+3];"
    p = Parser(Lexer(input))
    prog = p.parse_program()
    assert_no_parser_errors(p.errors)
    assert isinstance(prog.statements[0], ExpressionStatement)
    assert len(prog.statements[0].expression.elements) == 3
    assert_integer_literal(prog.statements[0].expression.elements[0], 1)
    assert_infix_expression(prog.statements[0].expression.elements[1], 2, "*", 2)
    assert_infix_expression(prog.statements[0].expression.elements[2], 3, "+", 3)


def test_string_literal_expression():
    input = """
  "Hello Space!"
  """
    p = Parser(Lexer(input))
    prog = p.parse_program()
    assert_no_parser_errors(p.errors)
    assert prog.statements[0].expression.value == "Hello Space!"
    assert isinstance(prog.statements[0], ExpressionStatement)
    assert isinstance(prog.statements[0].expression, StringLiteral)


def test_let_statement():
    input = """
   let x = 5;
   let y = 10;
   let foobar = 838383;"""
    p = Parser(Lexer(input))

    prog = p.parse_program()

    assert_no_parser_errors(p.errors)

    assert (
            len(prog.statements) == 3
    ), "prog.statements does not contain 3 statements. got=%d" % (
        len(prog.statements)
    )

    tests = ["x", "y", "foobar"]
    for i, tt in enumerate(tests):
        stmt = prog.statements[i]
        assert (
                stmt.token_literal() == "let"
        ), "stmt.token_literal not 'let'. got=%s" % (stmt.token_literal())
        assert stmt.name.value == tt, "stmt.name.value not '%s'. got=%s" % (
            tt, stmt.name.value
        )
        assert stmt.name.token_literal() == tt, "stmt.name not '%s'. got=%s" % (
            tt, stmt.name
        )


def test_let_expressions():
    tests = [
        ("let x = 5;", "x", 5),
        ("let y = true;", "y", True),
        ("let foobar = y;", "foobar", "y"),
    ]
    for tt in tests:
        p = Parser(Lexer(tt[0]))
        prog = p.parse_program()
        assert_no_parser_errors(p.errors)

        assert len(prog.statements) == 1
        
        stmt = prog.statements[0]
        assert isinstance(stmt, LetStatement)
        assert_literal_expression(stmt.value, tt[2])


def test_return_statement():
    input = """
   return 1;
   return 10;
   return 11;
   """
    p = Parser(Lexer(input))
    prog = p.parse_program()
    assert_no_parser_errors(p.errors)

    assert len(prog.statements) == 3

    for stmt in prog.statements:
        assert isinstance(stmt, ReturnStatement)
        assert (stmt.token_literal() == "return")


def test_parser_errors():
    input = """let """
    p = Parser(Lexer(input))
    p.parse_program()
    assert len(p.errors) == 1
    assert p.errors[0] is not None


def test_identifier_expression():
    input = "foobar;"

    p = Parser(Lexer(input))
    prog = p.parse_program()
    assert_no_parser_errors(p.errors)

    assert len(prog.statements) == 1
    assert isinstance(prog.statements[0], ExpressionStatement)
    assert prog.statements[0].expression.value == "foobar"
    assert prog.statements[0].token_literal() == "foobar"


def test_integer_literal_expression():
    input = "6;"
    p = Parser(Lexer(input))
    prog = p.parse_program()
    assert_no_parser_errors(p.errors)
    assert len(prog.statements) == 1

    assert isinstance(prog.statements[0], ExpressionStatement)
    assert isinstance(prog.statements[0].expression, Expression)
    assert prog.statements[0].expression.value == 6
    assert prog.statements[0].expression.token_literal() == "6"


def test_parsing_prefix_expressions():
    tests = [
        ("!5;", "!", 5),
        ("-15;", "-", 15),
        ("!true;", "!", True),
        ("!false;", "!", False),
    ]

    for t in tests:
        p = Parser(Lexer(t[0]))
        prog = p.parse_program()
        assert_no_parser_errors(p.errors)
        assert len(prog.statements) == 1
        assert isinstance(prog.statements[0], ExpressionStatement)
        
        assert isinstance(prog.statements[0].expression, Expression)
        assert prog.statements[0].expression.operator == t[1]
        assert_literal_expression(prog.statements[0].expression.right, t[2])


def test_parsing_infix_expressions():
    tests = [
        ("5 + 5;", 5, "+", 5),
        ("5 - 5;", 5, "-", 5),
        ("5 * 5;", 5, "*", 5),
        ("5 / 5;", 5, "/", 5),
        ("5 > 5;", 5, ">", 5),
        ("5 < 5;", 5, "<", 5),
        ("5 == 5;", 5, "==", 5),
        ("5 != 5;", 5, "!=", 5),
        ("true == true", True, "==", True),
        ("false == false", False, "==", False),
        ("false == false", False, "==", False),
    ]
    for t in tests:
        p = Parser(Lexer(t[0]))
        prog = p.parse_program()
        assert_no_parser_errors(p.errors)
        assert len(prog.statements) == 1
        assert isinstance(prog.statements[0], ExpressionStatement)
        assert isinstance(prog.statements[0].expression, Expression)
        assert_literal_expression(prog.statements[0].expression.left, t[1])
        assert prog.statements[0].expression.operator == t[2]
        assert_literal_expression(prog.statements[0].expression.right, t[3])


def test_operator_precedence():
    tests = [
        ("-pavel * kimchi", "((-pavel) * kimchi)"),
        ("!-pavel", "(!(-pavel))"),
        ("pavel + kimchi + soda", "((pavel + kimchi) + soda)"),
        ("pavel + kimchi - soda", "((pavel + kimchi) - soda)"),
        ("pavel * kimchi * soda", "((pavel * kimchi) * soda)"),
        ("pavel * kimchi / soda", "((pavel * kimchi) / soda)"),
        ("pavel + kimchi / soda", "(pavel + (kimchi / soda))"),
        (
            "pavel + kimchi * soda + love / london - yoyo",
            "(((pavel + (kimchi * soda)) + (love / london)) - yoyo)",
        ),
        ("77 + 25; -5 * 5", "(77 + 25)((-5) * 5)"),
        ("5 > 25 == 77 < 25", "((5 > 25) == (77 < 25))"),
        ("5 < 25 != 77 > 25", "((5 < 25) != (77 > 25))"),
        (
            "77 + 25 * 5 == 77 * 9 + 25 * 5",
            "((77 + (25 * 5)) == ((77 * 9) + (25 * 5)))",
        ),
        (
            "77 + 25 * 5 == 77 * 9 + 25 * 5",
            "((77 + (25 * 5)) == ((77 * 9) + (25 * 5)))",
        ),
        ("true", "true"),
        ("false", "false"),
        ("3 > 5 == false", "((3 > 5) == false)"),
        ("3 < 5 == true", "((3 < 5) == true)"),
        ("1 + (2 + 3) + 4", "((1 + (2 + 3)) + 4)"),
        ("(5 + 5) * 2", "((5 + 5) * 2)"),
        ("2 / (5 + 5)", "(2 / (5 + 5))"),
        ("(5 + 5) * 2 * (5 + 5)", "(((5 + 5) * 2) * (5 + 5))"),
        ("-(5 + 5)", "(-(5 + 5))"),
        ("!(true == true)", "(!(true == true))"),
        ("a + add(b * c) + d", "((a + add((b * c))) + d)"),
        (
            "add(a, b, 1, 2 * 3, 4 + 5, add(6, 7 * 8))",
            "add(a, b, 1, (2 * 3), (4 + 5), add(6, (7 * 8)))",
        ),
        ("add(a + b + c * d / f + g)", "add((((a + b) + ((c * d) / f)) + g))"),
        ("a * [ 1, 2, 3, 4 ][ b * c ] * d ", "((a * ([1, 2, 3, 4][(b * c)])) * d)"),
        ("add( a * b[2], b[1], 2 * [1,2][1])", "add((a * (b[2])), (b[1]), (2 * ([1, 2][1])))"),
    ]
    for t in tests:
        p = Parser(Lexer(t[0]))
        prog = p.parse_program()
        assert_no_parser_errors(p.errors)
        assert str(prog) == t[1]


def test_boolean_expressions():
    tests = [
        ("true;", True),
        ("false;", False),
        # TODO: add more tests
        # ("3 > 5 == false", "((3 > 5) == false)"),
        # ("3 < 5 == true", "((3 < 5) == true)"),
    ]
    for tt in tests:
        p = Parser(Lexer(tt[0]))
        prog = p.parse_program()
        assert_no_parser_errors(p.errors)
        assert len(prog.statements) == 1
        
        stmt = prog.statements[0]
        assert isinstance(stmt, ExpressionStatement)
        assert isinstance(stmt.expression, Expression)
        assert stmt.expression.value == tt[1]


def test_if_expression():
    input = "if (x < y) { x }"
    p = Parser(Lexer(input))
    prog = p.parse_program()
    assert_no_parser_errors(p.errors)
    assert len(prog.statements) == 1
    assert isinstance(prog.statements[0], ExpressionStatement)
    
    assert isinstance(prog.statements[0].expression, IfExpression)
    assert_infix_expression(prog.statements[0].expression.condition, "x", "<", "y")
    assert len(prog.statements[0].expression.consequence.statements) == 1
    assert isinstance(prog.statements[0].expression.consequence.statements[0], ExpressionStatement)
    assert_identifier(prog.statements[0].expression.consequence.statements[0].expression, "x")
    assert prog.statements[0].expression.alternative is None


def test_if_else_expression():
    input = "if (x < y) { x } else { y }"
    p = Parser(Lexer(input))
    prog = p.parse_program()
    assert_no_parser_errors(p.errors)
    assert len(prog.statements) == 1
    assert prog.statements[0], ExpressionStatement
    assert isinstance(prog.statements[0].expression, IfExpression)
    assert_infix_expression(prog.statements[0].expression.condition, "x", "<", "y")
    assert len(prog.statements[0].expression.consequence.statements) == 1
    assert isinstance(prog.statements[0].expression.consequence.statements[0], ExpressionStatement)
    assert_identifier(prog.statements[0].expression.consequence.statements[0].expression, "x")


def test_function_literal():
    input = "fn(x, y) { x + y; }"
    p = Parser(Lexer(input))
    prog = p.parse_program()
    assert_no_parser_errors(p.errors)

    assert len(prog.statements) == 1
    assert isinstance(prog.statements[0], ExpressionStatement)
    assert isinstance(prog.statements[0].expression, FunctionLiteral)
    assert len(prog.statements[0].expression.parameters) == 2
    assert_literal_expression(prog.statements[0].expression.parameters[0], "x")
    assert_literal_expression(prog.statements[0].expression.parameters[1], "y")

    assert len(prog.statements[0].expression.body.statements) == 1
    assert isinstance(prog.statements[0].expression.body.statements[0], ExpressionStatement)
    assert_infix_expression(
        prog.statements[0].expression.body.statements[0].expression, "x", "+", "y"
    )


def test_function_parameter_parsing():
    tests = [
        {"input": "fn() {};", "expected_params": []},
        {"input": "fn(x) {};", "expected_params": ["x"]},
        {"input": "fn(x, y, z){};", "expected_params": ["x", "y", "z"]},
    ]
    for tt in tests:
        p = Parser(Lexer(tt["input"]))
        prog = p.parse_program()
        assert_no_parser_errors(p.errors)
        assert len(prog.statements) == 1
        assert isinstance(prog.statements[0], ExpressionStatement)
        assert isinstance(prog.statements[0].expression, FunctionLiteral)
        assert len(prog.statements[0].expression.parameters) == len(tt["expected_params"])
        for i, ident in enumerate(tt["expected_params"]):
            assert_literal_expression(
                prog.statements[0].expression.parameters[i], ident
            )


def test_call_expression():
    input = "add(1, 2 * 3, 4 + 5);"
    p = Parser(Lexer(input))
    prog = p.parse_program()
    assert_no_parser_errors(p.errors)
    assert len(prog.statements) == 1
    stmt = prog.statements[0]
    assert isinstance(stmt, ExpressionStatement)
    assert isinstance(stmt.expression, CallExpression)
    
    assert_identifier(stmt.expression.function, "add")
    assert len(stmt.expression.arguments) == 3
    assert_literal_expression(stmt.expression.arguments[0], 1)
    assert_infix_expression(stmt.expression.arguments[1], 2, "*", 3)
    assert_infix_expression(stmt.expression.arguments[2], 4, "+", 5)


def assert_identifier(exp, value):
    assert isinstance(exp, Identifier)
    assert exp.value == value
    assert exp.token_literal() == value


def assert_literal_expression(exp, expected):
    if type(expected) is int:
        assert_integer_literal(exp, expected)
    elif type(expected) is str:
        assert_identifier(exp, expected)
    elif type(expected) is bool:
        assert_boolean_literal(exp, expected)
    else:
        raise Exception("type of exp not handled. got=%s" % (type(exp)))


def assert_boolean_literal(exp, expected):
    assert isinstance(exp, Boolean)
    assert exp.value == expected
    assert exp.token_literal() == str(expected).lower()


def assert_infix_expression(exp, left, operator, right):
    assert isinstance(exp, InfixExpression)
    assert_literal_expression(exp.left, left)
    assert exp.operator == operator
    assert_literal_expression(exp.right, right)


def assert_no_parser_errors(errors):
    if len(errors) != 0:
        print("parser has %f errors" % (len(errors)))
        for err in errors:
            print("parser error: %s" % (err))
        assert False        


def assert_integer_literal(exp, value):
    assert isinstance(exp, IntegerLiteral)
    assert exp.value == value
    assert exp.token_literal() == str(value)
