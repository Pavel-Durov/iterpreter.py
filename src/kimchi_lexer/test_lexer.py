from src.kimchi_lexer import Lexer
from src.kimchi_tk import Tk


def test_next_token():
    input = """
     let five = 5;
    let ten = 10;
    let add = fn(x, y) {
        x + y;
    };
    let result = add(five, ten);
    !-/*5;
    5 < 10 > 5;
    if (5 < 10) {
        return true;
    } else {
        return false;
    }
    
    10 == 10; 
    10 != 9;
    "some-string-here"
    "another-string-there"
    [1, 2];
    {"foo": "bar"};
   
    while(true) {
      return 1;
    }
    
   """
    tests = [
        (Tk.LET, "let"),
        (Tk.IDENT, "five"),
        (Tk.ASSIGN, "="),
        (Tk.INT, "5"),
        (Tk.SEMICOLON, ";"),
        (Tk.LET, "let"),
        (Tk.IDENT, "ten"),
        (Tk.ASSIGN, "="),
        (Tk.INT, "10"),
        (Tk.SEMICOLON, ";"),
        (Tk.LET, "let"),
        (Tk.IDENT, "add"),
        (Tk.ASSIGN, "="),
        (Tk.FUNCTION, "fn"),
        (Tk.LPAREN, "("),
        (Tk.IDENT, "x"),
        (Tk.COMMA, ","),
        (Tk.IDENT, "y"),
        (Tk.RPAREN, ")"),
        (Tk.LBRACE, "{"),
        (Tk.IDENT, "x"),
        (Tk.PLUS, "+"),
        (Tk.IDENT, "y"),
        (Tk.SEMICOLON, ";"),
        (Tk.RBRACE, "}"),
        (Tk.SEMICOLON, ";"),
        (Tk.LET, "let"),
        (Tk.IDENT, "result"),
        (Tk.ASSIGN, "="),
        (Tk.IDENT, "add"),
        (Tk.LPAREN, "("),
        (Tk.IDENT, "five"),
        (Tk.COMMA, ","),
        (Tk.IDENT, "ten"),
        (Tk.RPAREN, ")"),
        (Tk.SEMICOLON, ";"),
        (Tk.BANG, "!"),
        (Tk.MINUS, "-"),
        (Tk.SLASH, "/"),
        (Tk.ASTERISK, "*"),
        (Tk.INT, "5"),
        (Tk.SEMICOLON, ";"),
        (Tk.INT, "5"),
        (Tk.LT, "<"),
        (Tk.INT, "10"),
        (Tk.GT, ">"),
        (Tk.INT, "5"),
        (Tk.SEMICOLON, ";"),
        # if
        (Tk.IF, "if"),
        (Tk.LPAREN, "("),
        (Tk.INT, "5"),
        (Tk.LT, "<"),
        (Tk.INT, "10"),
        (Tk.RPAREN, ")"),
        (Tk.LBRACE, "{"),
        (Tk.RETURN, "return"),
        (Tk.TRUE, "true"),
        (Tk.SEMICOLON, ";"),
        (Tk.RBRACE, "}"),
        (Tk.ELSE, "else"),
        (Tk.LBRACE, "{"),
        (Tk.RETURN, "return"),
        (Tk.FALSE, "false"),
        (Tk.SEMICOLON, ";"),
        (Tk.RBRACE, "}"),
        (Tk.INT, "10"),
        (Tk.EQ, "=="),
        (Tk.INT, "10"),
        (Tk.SEMICOLON, ";"),
        (Tk.INT, "10"),
        (Tk.NOT_EQ, "!="),
        (Tk.INT, "9"),
        (Tk.SEMICOLON, ";"),
        (Tk.STRING, "some-string-here"),
        (Tk.STRING, "another-string-there"),
        # array
        (Tk.LBRACKET, "["),
        (Tk.INT, "1"),
        (Tk.COMMA, ","),
        (Tk.INT, "2"),
        (Tk.RBRACKET, "]"),
        (Tk.SEMICOLON, ";"),
        # hashmap
        (Tk.LBRACE, "{"),
        (Tk.STRING, "foo"),
        (Tk.COLON, ":"),
        (Tk.STRING, "bar"),
        (Tk.RBRACE, "}"),
        (Tk.SEMICOLON, ";"),
        # while
        (Tk.WHILE, "while"),
        (Tk.LPAREN, "("),
        (Tk.TRUE, "true"),
        (Tk.RPAREN, ")"),
        (Tk.LBRACE, "{"),
        (Tk.RETURN, "return"),
        (Tk.INT, "1"),
        (Tk.SEMICOLON, ";"),
        (Tk.RBRACE, "}"),
        # fin :)
        (Tk.EOF, ""),
    ]
    lex = Lexer(input)
    for tt in tests:
        tok = lex.next_token()
        assert tok.type == tt[0]
        assert tok.type == tt[0]
        assert tok.literal == tt[1]
