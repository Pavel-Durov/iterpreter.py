from src.awk_lexer import Lexer
from src.awk_parser import Parser


def test_string():
    p = Parser(Lexer("let myVar = 234;"))
    prog = p.parse_program()
    assert str(prog) == "let myVar = 234;"
