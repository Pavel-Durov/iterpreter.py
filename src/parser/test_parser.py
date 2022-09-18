from cgi import test
from src.ast import Program, LetStatement, Identifier
from src.lexer import Lexer
from src.parser import Parser

def test_let_statement():
  input = """
   let x = 5;
   let y = 10;
   let foobar = 838383;"""
  
  l = Lexer(input)
  p = Parser(l)
  prog = p.parse_program()
  assert prog != None, "ParseProgram() returned None"
  print(prog.statements)
  assert len(prog.statements) == 3, "prog.statements does not contain 3 statements. got={}".format(len(prog.statements))

  tests = ["x", "y", "foobar"]  
  for i, tt in enumerate(tests):
    stmt = prog.statements[i]
    assert stmt.token_literal() == "let", "stmt.token_literal not 'let'. got={}".format(stmt.token_literal())
    assert stmt.name.value == tt, "stmt.name.value not '{}'. got={}".format(tt, stmt.name.value)
    assert stmt.name.token_literal() == tt, "stmt.name not '{}'. got={}".format(tt, stmt.name)
  

