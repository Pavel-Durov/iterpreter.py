from src.kimchi_ast import (
    Boolean,
    CallExpression,
    ExpressionStatement,
    FunctionLiteral,
    Identifier,
    IfExpression,
    InfixExpression,
    IntegerLiteral,
    LetStatement,
    ReturnStatement,
    Expression,
)
from src.kimchi_lexer import Lexer
from src.kimchi_parser import Parser


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
    ), "prog.statements does not contain 3 statements. got={}".format(
        len(prog.statements)
    )

    tests = ["x", "y", "foobar"]
    for i, tt in enumerate(tests):
        stmt = prog.statements[i]
        assert (
                stmt.token_literal() == "let"
        ), "stmt.token_literal not 'let'. got={}".format(stmt.token_literal())
        assert stmt.name.value == tt, "stmt.name.value not '{}'. got={}".format(
            tt, stmt.name.value
        )
        assert stmt.name.token_literal() == tt, "stmt.name not '{}'. got={}".format(
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

        assert (
                len(prog.statements) == 1
        ), "prog.statements does not contain 1 statements. got={}".format(
            len(prog.statements)
        )
        stmt = prog.statements[0]
        assert isinstance(
            stmt, LetStatement
        ), "stmt is not LetStatement. got={}".format(type(stmt))
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

    assert (
            len(prog.statements) == 3
    ), "prog.statements does not contain 3 statements. got={}".format(
        len(prog.statements)
    )

    for stmt in prog.statements:
        assert isinstance(
            stmt, ReturnStatement
        ), "stmt is not ReturnStatement. got={}".format(type(stmt))
        assert (
                stmt.token_literal() == "return"
        ), "stmt.token_literal not 'return'. got={}".format(stmt.token_literal())


def test_parser_errors():
    input = """let """
    p = Parser(Lexer(input))
    p.parse_program()
    assert len(p.errors) == 1, "parser has {} errors".format(len(p.errors))
    assert p.errors[0] is not None


def test_identifier_expression():
    input = "foobar;"

    p = Parser(Lexer(input))
    prog = p.parse_program()
    assert_no_parser_errors(p.errors)

    assert (
            len(prog.statements) == 1
    ), "prog.statements does not contain 1 statements. got={}".format(
        len(prog.statements)
    )

    assert isinstance(
        prog.statements[0], ExpressionStatement
    ), "prog.statements[0] is not Identifier. got={}".format(type(prog.statements[0]))
    assert (
            prog.statements[0].expression.value == "foobar"
    ), "prog.statements[0].value not {}. got={}".format(
        "foobar", prog.statements[0].value
    )
    assert (
            prog.statements[0].token_literal() == "foobar"
    ), "prog.statements[0] not {}. got={}".format("foobar", prog.statements[0])


def test_integer_literal_expression():
    input = "6;"
    p = Parser(Lexer(input))
    prog = p.parse_program()
    assert_no_parser_errors(p.errors)
    assert (
            len(prog.statements) == 1
    ), "prog.statements does not contain 1 statements. got={}".format(
        len(prog.statements)
    )

    assert isinstance(
        prog.statements[0], ExpressionStatement
    ), "prog.statements[0] is not Identifier. got={}".format(type(prog.statements[0]))
    assert isinstance(
        prog.statements[0].expression, Expression
    ), "prog.statements[0].expression is not Expression. got={}".format(
        type(prog.statements[0].expression)
    )
    assert (
            prog.statements[0].expression.value == 6
    ), "prog.statements[0].value not {}. got={}".format(6, prog.statements[0].value)
    assert (
            prog.statements[0].expression.token_literal() == "6"
    ), "prog.statements[0] not {}. got={}".format(6, prog.statements[0])


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
        assert (
                len(prog.statements) == 1
        ), "prog.statements does not contain 1 statements. got={}".format(
            len(prog.statements)
        )
        assert isinstance(
            prog.statements[0], ExpressionStatement
        ), "prog.statements[0] is not ExpressionStatement. got={}".format(
            type(prog.statements[0])
        )
        assert isinstance(
            prog.statements[0].expression, Expression
        ), "prog.statements[0].expression is not Expression. got={}".format(
            type(prog.statements[0].expression)
        )
        assert (
                prog.statements[0].expression.operator == t[1]
        ), "prog.statements[0].expression.operator is not {}. got={}".format(
            t[1], prog.statements[0].expression.operator
        )
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
        assert (
                len(prog.statements) == 1
        ), "prog.statements does not contain 1 statements. got={}".format(
            len(prog.statements)
        )
        assert isinstance(
            prog.statements[0], ExpressionStatement
        ), "prog.statements[0] is not Identifier. got={}".format(
            type(prog.statements[0])
        )
        assert isinstance(
            prog.statements[0].expression, Expression
        ), "prog.statements[0].expression is not Expression. got={}".format(
            type(prog.statements[0].expression)
        )
        assert_literal_expression(prog.statements[0].expression.left, t[1])
        assert (
                prog.statements[0].expression.operator == t[2]
        ), "prog.statements[0].expression.operator is not {}. got={}".format(
            t[2], prog.statements[0].expression.operator
        )
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
    ]
    for t in tests:
        p = Parser(Lexer(t[0]))
        prog = p.parse_program()
        assert_no_parser_errors(p.errors)
        assert str(prog) == t[1], "expected={}, got={}".format(t[1], str(prog))


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
        assert (
                len(prog.statements) == 1
        ), "prog.statements does not contain 1 statements. got={}".format(
            len(prog.statements)
        )
        stmt = prog.statements[0]
        assert isinstance(
            stmt, ExpressionStatement
        ), "stmt is not ExpressionStatement. got={}".format(type(stmt))
        assert isinstance(
            stmt.expression, Expression
        ), "stmt.expression is not Expression. got={}".format(type(stmt.expression))
        assert (
                stmt.expression.value == tt[1]
        ), "stmt.expression.value is not {}. got={}".format(
            tt[1], stmt.expression.value
        )


def test_if_expression():
    input = "if (x < y) { x }"
    p = Parser(Lexer(input))
    prog = p.parse_program()
    assert_no_parser_errors(p.errors)
    assert (
            len(prog.statements) == 1
    ), "prog.statements does not contain 1 statements. got={}".format(
        len(prog.statements)
    )
    assert isinstance(
        prog.statements[0], ExpressionStatement
    ), "prog.statements[0] is not ExpressionStatement. got={}".format(
        type(prog.statements[0])
    )
    assert isinstance(
        prog.statements[0].expression, IfExpression
    ), "prog.statements[0].expression is not IfExpression. got={}".format(
        type(prog.statements[0].expression)
    )
    assert_infix_expression(prog.statements[0].expression.condition, "x", "<", "y")
    assert (
            len(prog.statements[0].expression.consequence.statements) == 1
    ), "consequence is not 1 statements. got={}".format(
        len(prog.statements[0].expression.consequence.statements)
    )
    assert isinstance(
        prog.statements[0].expression.consequence.statements[0], ExpressionStatement
    ), "prog.statements[0].expression.consequence.statements[0] is not ExpressionStatement. got={}".format(
        type(prog.statements[0].expression.consequence.statements[0])
    )
    assert_identifier(
        prog.statements[0].expression.consequence.statements[0].expression, "x"
    )
    assert (
            prog.statements[0].expression.alternative is None
    ), "prog.statements[0].expression.alternative.statements was not None. got={}".format(
        prog.statements[0].expression.alternative
    )


def test_if_else_expression():
    input = "if (x < y) { x } else { y }"
    p = Parser(Lexer(input))
    prog = p.parse_program()
    assert_no_parser_errors(p.errors)
    assert (
            len(prog.statements) == 1
    ), "prog.statements does not contain 1 statements. got={}".format(
        len(prog.statements)
    )
    assert isinstance(
        prog.statements[0], ExpressionStatement
    ), "prog.statements[0] is not ExpressionStatement. got={}".format(
        type(prog.statements[0])
    )
    assert isinstance(
        prog.statements[0].expression, IfExpression
    ), "prog.statements[0].expression is not IfExpression. got={}".format(
        type(prog.statements[0].expression)
    )
    assert_infix_expression(prog.statements[0].expression.condition, "x", "<", "y")
    assert (
            len(prog.statements[0].expression.consequence.statements) == 1
    ), "consequence is not 1 statements. got={}".format(
        len(prog.statements[0].expression.consequence.statements)
    )
    assert isinstance(
        prog.statements[0].expression.consequence.statements[0], ExpressionStatement
    ), "prog.statements[0].expression.consequence.statements[0] is not ExpressionStatement. got={}".format(
        type(prog.statements[0].expression.consequence.statements[0])
    )
    assert_identifier(
        prog.statements[0].expression.consequence.statements[0].expression, "x"
    )
    assert (
            prog.statements[0].expression.alternative is not None
    ), "prog.statements[0].expression.alternative.statements was not None. got={}".format(
        prog.statements[0].expression.alternative
    )


def test_function_literal():
    input = "fn(x, y) { x + y; }"
    p = Parser(Lexer(input))
    prog = p.parse_program()
    assert_no_parser_errors(p.errors)

    assert (
            len(prog.statements) == 1
    ), "prog.statements does not contain 1 statements. got={}".format(
        len(prog.statements)
    )
    assert isinstance(
        prog.statements[0], ExpressionStatement
    ), "prog.statements[0] is not ExpressionStatement. got={}".format(
        type(prog.statements[0])
    )
    assert isinstance(
        prog.statements[0].expression, FunctionLiteral
    ), "prog.statements[0].expression is not FunctionLiteral. got={}".format(
        type(prog.statements[0].expression)
    )
    assert (
            len(prog.statements[0].expression.parameters) == 2
    ), "function literal parameters wrong. want 2, got={}".format(
        len(prog.statements[0].expression.parameters)
    )
    assert_literal_expression(prog.statements[0].expression.parameters[0], "x")
    assert_literal_expression(prog.statements[0].expression.parameters[1], "y")

    assert (
            len(prog.statements[0].expression.body.statements) == 1
    ), "function body statements has not 1 statements. got={}".format(
        len(prog.statements[0].expression.body.statements)
    )
    assert isinstance(
        prog.statements[0].expression.body.statements[0], ExpressionStatement
    ), "function body statement is not ExpressionStatement. got={}".format(
        type(prog.statements[0].expression.body.statements[0])
    )
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
        assert (
                len(prog.statements) == 1
        ), "prog.statements does not contain 1 statements. got={}".format(
            len(prog.statements)
        )
        assert isinstance(
            prog.statements[0], ExpressionStatement
        ), "prog.statements[0] is not ExpressionStatement. got={}".format(
            type(prog.statements[0])
        )
        assert isinstance(
            prog.statements[0].expression, FunctionLiteral
        ), "prog.statements[0].expression is not FunctionLiteral. got={}".format(
            type(prog.statements[0].expression)
        )
        assert len(prog.statements[0].expression.parameters) == len(
            tt["expected_params"]
        ), "function literal parameters wrong. want {}, got={}".format(
            len(tt["expected_params"]), len(prog.statements[0].expression.parameters)
        )
        for i, ident in enumerate(tt["expected_params"]):
            assert_literal_expression(
                prog.statements[0].expression.parameters[i], ident
            )


def test_call_expression():
    input = "add(1, 2 * 3, 4 + 5);"
    p = Parser(Lexer(input))
    prog = p.parse_program()
    assert_no_parser_errors(p.errors)
    assert (
            len(prog.statements) == 1
    ), "prog.statements does not contain 1 statements. got={}".format(
        len(prog.statements)
    )
    stmt = prog.statements[0]
    assert isinstance(
        stmt, ExpressionStatement
    ), "stmt is not ExpressionStatement. got={}".format(type(stmt))
    assert isinstance(
        stmt.expression, CallExpression
    ), "stmt.expression is not CallExpression. got={}".format(type(stmt.expression))
    assert_identifier(stmt.expression.function, "add")
    assert (
            len(stmt.expression.arguments) == 3
    ), "wrong length of arguments. got={}".format(len(stmt.expression.arguments))
    assert_literal_expression(stmt.expression.arguments[0], 1)
    assert_infix_expression(stmt.expression.arguments[1], 2, "*", 3)
    assert_infix_expression(stmt.expression.arguments[2], 4, "+", 5)


def assert_identifier(exp, value):
    assert isinstance(exp, Identifier), "exp is not Identifier. got={}".format(
        type(exp)
    )
    assert exp.value == value, "exp.value is not {}. got={}".format(value, exp.value)
    assert exp.token_literal() == value, "exp.token_literal is not {}. got={}".format(
        value, exp.token_literal()
    )


def assert_literal_expression(exp, expected):
    if type(expected) is int:
        assert_integer_literal(exp, expected)
    elif type(expected) is str:
        assert_identifier(exp, expected)
    elif type(expected) is bool:
        assert_boolean_literal(exp, expected)
    else:
        raise Exception("type of exp not handled. got={}".format(type(exp)))


def assert_boolean_literal(exp, expected):
    assert isinstance(exp, Boolean), "exp is not Boolean. got={}".format(type(exp))
    assert exp.value == expected, "exp.value is not {}. got={}".format(
        expected, exp.value
    )
    assert (
            exp.token_literal() == str(expected).lower()
    ), "exp.token_literal is not {}. got={}".format(expected, exp.token_literal())


def assert_infix_expression(exp, left, operator, right):
    assert isinstance(
        exp, InfixExpression
    ), "exp is not InfixExpression. got={}".format(type(exp))
    assert_literal_expression(exp.left, left)
    assert exp.operator == operator, "exp.operator is not {}. got={}".format(
        operator, exp.operator
    )
    assert_literal_expression(exp.right, right)


def assert_no_parser_errors(errors):
    if len(errors) != 0:
        print("parser has {} errors".format(len(errors)))
        for err in errors:
            print("parser error: {}".format(err))
        assert False, "parser has {} errors".format(len(errors))


def assert_integer_literal(exp, value):
    assert isinstance(exp, IntegerLiteral), "exp is not IntegerLiteral. got={}".format(
        type(exp)
    )
    assert exp.value == value, "exp.value is not {}. got={}".format(value, exp.value)
    assert exp.token_literal() == str(
        value
    ), "exp.token_literal is not {}. got={}".format(value, exp.token_literal())
