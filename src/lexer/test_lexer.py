from src.lexer import Lexer
from src.token import Token


def test_some():
    input = """
    let five = 5;
    let ten = 10;
      let add = fn(x, y) {
        x + y;
    };
    let result = add(five, ten);
   """
    tests = [
        (Token.LET, "let"),
        (Token.IDENT, "five"),
        (Token.ASSIGN, "="),
        (Token.INT, "5"),
        (Token.SEMICOLON, ";"),
        (Token.LET, "let"),
        (Token.IDENT, "ten"),
        (Token.ASSIGN, "="),
        (Token.INT, "10"),
        (Token.SEMICOLON, ";"),
        (Token.LET, "let"),
        (Token.IDENT, "add"),
        (Token.ASSIGN, "="),
        (Token.FUNCTION, "fn"),
        (Token.LPAREN, "("),
        (Token.IDENT, "x"),
        (Token.COMMA, ","),
        (Token.IDENT, "y"),
        (Token.RPAREN, ")"),
        (Token.LBRACE, "{"),
        (Token.IDENT, "x"),
        (Token.PLUS, "+"),
        (Token.IDENT, "y"),
        (Token.SEMICOLON, ";"),
        (Token.RBRACE, "}"),
        (Token.SEMICOLON, ";"),
        (Token.LET, "let"),
        (Token.IDENT, "result"),
        (Token.ASSIGN, "="),
        (Token.IDENT, "add"),
        (Token.LPAREN, "("),
        (Token.IDENT, "five"),
        (Token.COMMA, ","),
        (Token.IDENT, "ten"),
        (Token.RPAREN, ")"),
        (Token.SEMICOLON, ";"),
        (Token.EOF, ""),
    ]
    l = Lexer(input)
    for tt in tests:
        tok = l.next_token()
        print("@@@", tok.type, tok.literal)
        # assert tok.type == tt[0], f"tokentype wrong. expected={tt[0]}, got={tok.type}"
        # assert tok.literal == tt[1], f"expected {tt[1]}, got {tok.literal}"
