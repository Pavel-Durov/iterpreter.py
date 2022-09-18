from cgi import test
from src.ast import Program, LetStatement, Identifier
from src.ast.ast import ReturnStatement
from src.lexer import Lexer
from src.parser import Parser

def test_let_statement():
  input = """
   let x = 5;
   let y = 10;
   let foobar = 838383;"""
  p = Parser(Lexer(input))
  
  prog = p.parse_program()
  
  assert_parser_has_no_errors(p.errors)

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
  
  assert_parser_has_no_errors(p.errors)

  assert len(prog.statements) == 3, "prog.statements does not contain 3 statements. got={}".format(len(prog.statements))

  tests = ["x", "y", "foobar"]  
  for stmt in prog.statements:
    assert isinstance(stmt, ReturnStatement), "stmt is not ReturnStatement. got={}".format(type(stmt))
    assert stmt.token_literal() == "return", "stmt.token_literal not 'return'. got={}".format(stmt.token_literal())




def test_parser_errors():
  input = """
   let = 838383;"""
  p = Parser(Lexer(input))
  
  prog = p.parse_program()
  assert len(p.errors) == 1, "parser has {} errors".format(len(p.errors))
  assert p.errors[0] is not None


def assert_parser_has_no_errors(errors):

    if len(errors) != 0:
        print("parser has {} errors".format(len(errors)))
        for err in errors:
            print("parser error: {}".format(err))
        assert False, "parser has {} errors".format(len(errors))

