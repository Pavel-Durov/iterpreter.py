from src.ast.ast import ExpressionStatement, IntegerLiteral, ReturnStatement, Expression
from src.lexer import Lexer
from src.parser import Parser

def test_let_statement():
  input = """
   let x = 5;
   let y = 10;
   let foobar = 838383;"""
  p = Parser(Lexer(input))
  
  prog = p.parse_program()
  
  assert_no_parser_errors(p.errors)

  assert len(prog.statements) == 3, "prog.statements does not contain 3 statements. got={}".format(len(prog.statements))

  tests = ["x", "y", "foobar"]  
  for i, tt in enumerate(tests):
    stmt = prog.statements[i]
    assert stmt.token_literal() == "let", "stmt.token_literal not 'let'. got={}".format(stmt.token_literal())
    assert stmt.name.value == tt, "stmt.name.value not '{}'. got={}".format(tt, stmt.name.value)
    assert stmt.name.token_literal() == tt, "stmt.name not '{}'. got={}".format(tt, stmt.name)


def test_return_statement():
  input = """
   return 1;
   return 10;
   return 11;
   """
  p = Parser(Lexer(input))
  
  prog = p.parse_program()
  
  assert_no_parser_errors(p.errors)

  assert len(prog.statements) == 3, "prog.statements does not contain 3 statements. got={}".format(len(prog.statements))

  tests = ["x", "y", "foobar"]  
  for stmt in prog.statements:
    assert isinstance(stmt, ReturnStatement), "stmt is not ReturnStatement. got={}".format(type(stmt))
    assert stmt.token_literal() == "return", "stmt.token_literal not 'return'. got={}".format(stmt.token_literal())




# def test_parser_errors():
#   input = """
#    let = 838383;"""
#   p = Parser(Lexer(input))
  
#   prog = p.parse_program()
#   assert len(p.errors) == 1, "parser has {} errors".format(len(p.errors))
#   assert p.errors[0] is not None


def assert_no_parser_errors(errors):

    if len(errors) != 0:
        print("parser has {} errors".format(len(errors)))
        for err in errors:
            print("parser error: {}".format(err))
        assert False, "parser has {} errors".format(len(errors))

def test_identifier_expression():
    input = "foobar;"

    p = Parser(Lexer(input))
    prog = p.parse_program()
    assert_no_parser_errors(p.errors)

    assert len(prog.statements) == 1, "prog.statements does not contain 1 statements. got={}".format(len(prog.statements))
    
    assert isinstance(prog.statements[0], ExpressionStatement), "prog.statements[0] is not Identifier. got={}".format(type(prog.statements[0]))
    assert prog.statements[0].expression.value == "foobar", "prog.statements[0].value not {}. got={}".format("foobar", prog.statements[0].value)
    assert prog.statements[0].token_literal() == "foobar", "prog.statements[0] not {}. got={}".format("foobar", prog.statements[0])

def test_integer_literal_expression():
    input = "6;"
    p = Parser(Lexer(input))
    prog = p.parse_program()
    assert_no_parser_errors(p.errors)
    assert len(prog.statements)==1, "prog.statements does not contain 1 statements. got={}".format(len(prog.statements))

    assert isinstance(prog.statements[0], ExpressionStatement), "prog.statements[0] is not Identifier. got={}".format(type(prog.statements[0]))
    assert isinstance(prog.statements[0].expression, Expression), "prog.statements[0].expression is not Expression. got={}".format(type(prog.statements[0].expression))
    assert prog.statements[0].expression.value == 6, "prog.statements[0].value not {}. got={}".format(6, prog.statements[0].value)
    assert prog.statements[0].expression.token_literal() == '6', "prog.statements[0] not {}. got={}".format(6, prog.statements[0])
    

def test_parsing_prefix_expressions():
  tests = [("!5;", "!", 5), ("-15;", "-", 15)]

  for t in tests:
      p = Parser(Lexer(t[0]))
      prog = p.parse_program()
      assert_no_parser_errors(p.errors)
      assert len(prog.statements) == 1, "prog.statements does not contain 1 statements. got={}".format(len(prog.statements))
      assert isinstance(prog.statements[0], ExpressionStatement), "prog.statements[0] is not ExpressionStatement. got={}".format(type(prog.statements[0]))
      assert isinstance(prog.statements[0].expression, Expression), "prog.statements[0].expression is not Expression. got={}".format(type(prog.statements[0].expression))
      assert prog.statements[0].expression.operator == t[1], "prog.statements[0].expression.operator is not {}. got={}".format(t[1], prog.statements[0].expression.operator)
      assert_integer_literal(prog.statements[0].expression.right, t[2])

def assert_integer_literal(exp, value):
  assert isinstance(exp, IntegerLiteral), "exp is not IntegerLiteral. got={}".format(type(exp))
  assert exp.value == value, "exp.value is not {}. got={}".format(value, exp.value)
  assert exp.token_literal() == str(value), "exp.token_literal is not {}. got={}".format(value, exp.token_literal())


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
    ]
    for t in tests:
      p = Parser(Lexer(t[0]))
      prog = p.parse_program()
      assert_no_parser_errors(p.errors)
      assert len(prog.statements)==1, "prog.statements does not contain 1 statements. got={}".format(len(prog.statements))
      assert isinstance(prog.statements[0], ExpressionStatement), "prog.statements[0] is not Identifier. got={}".format(type(prog.statements[0]))
      assert isinstance(prog.statements[0].expression, Expression), "prog.statements[0].expression is not Expression. got={}".format(type(prog.statements[0].expression))
      assert_integer_literal(prog.statements[0].expression.left, t[1])
      assert prog.statements[0].expression.operator == t[2], "prog.statements[0].expression.operator is not {}. got={}".format(t[2], prog.statements[0].expression.operator)
      assert_integer_literal(prog.statements[0].expression.right, t[3])

def test_operator_precedence():
  tests = [
    ("-pavel * kimchi", "((-pavel) * kimchi)"),
    ("!-pavel", "(!(-pavel))"),
    ("pavel + kimchi + soda", "((pavel + kimchi) + soda)"),
    ("pavel + kimchi - soda", "((pavel + kimchi) - soda)" ),
    ("pavel * kimchi * soda", "((pavel * kimchi) * soda)"),
    ("pavel * kimchi / soda","((pavel * kimchi) / soda)"),
    ("pavel + kimchi / soda", "(pavel + (kimchi / soda))"),
    ("pavel + kimchi * soda + love / london - yoyo",  "(((pavel + (kimchi * soda)) + (love / london)) - yoyo)"),
    ("77 + 25; -5 * 5", "(77 + 25)((-5) * 5)"),
    ("5 > 25 == 77 < 25", "((5 > 25) == (77 < 25))"),
    ("5 < 25 != 77 > 25", "((5 < 25) != (77 > 25))"),
    ("77 + 25 * 5 == 77 * 9 + 25 * 5", "((77 + (25 * 5)) == ((77 * 9) + (25 * 5)))"),
    ("77 + 25 * 5 == 77 * 9 + 25 * 5", "((77 + (25 * 5)) == ((77 * 9) + (25 * 5)))")
  ]
  

  for t in tests:
    p = Parser(Lexer(t[0]))
    prog = p.parse_program()
    assert_no_parser_errors(p.errors)
    print('@@@', str(prog))
    assert str(prog) == t[1], "expected={}, got={}".format(t[1], str(prog))
