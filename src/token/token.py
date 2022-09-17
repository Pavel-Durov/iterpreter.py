class Token:
    FUNCTION = "function"
    LET = "let"

    ILLEGAL = "ILLEGAL"
    EOF = "EOF"

    # Identifiers + literals
    IDENT = "IDENT"  # add, foobar, x, y, ...
    INT = "INT"

    # Operators
    ASSIGN = "="
    PLUS = "+"

    # Delimiters
    COMMA = ","
    SEMICOLON = ";"
    LPAREN = "("
    RPAREN = ")"
    LBRACE = "{"
    RBRACE = "}"

    # Keywords
    FUNCTION = "FUNCTION"
    LET = "LET"

    keywords = {
      "fn": FUNCTION,
      "let": LET, 
    }

    def __init__(self, type, literal) -> None:
        self.type = type
        self.literal = literal
    
    def lookup_ident(self, ident):
        if ident in self.keywords:
            return self.keywords[ident]
        return self.IDENT
