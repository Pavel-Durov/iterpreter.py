from src.kimchi_tk import Tk


class Lexer:
    def __init__(self, input):
        self.input = input
        self.position = 0
        self.read_position = 0
        self.ch = ""
        self.read_char()

    def read_char(self):
        if self.read_position >= len(self.input):
            self.ch = ""
        else:
            self.ch = self.input[self.read_position]
        self.position = self.read_position
        self.read_position += 1

    def skip_whitespace(self):
        while self.ch == " " or self.ch == "\t" or self.ch == "\r" or self.ch == "\n":
            self.read_char()

    def next_token(self):
        tok = Tk(None, None)
        self.skip_whitespace()

        if self.ch == ";":
            tok = Tk(Tk.SEMICOLON, self.ch)
        elif self.ch == "(":
            tok = Tk(Tk.LPAREN, self.ch)
        elif self.ch == ")":
            tok = Tk(Tk.RPAREN, self.ch)
        elif self.ch == ",":
            tok = Tk(Tk.COMMA, self.ch)
        elif self.ch == "+":
            tok = Tk(Tk.PLUS, self.ch)
        elif self.ch == "{":
            tok = Tk(Tk.LBRACE, self.ch)
        elif self.ch == "}":
            tok = Tk(Tk.RBRACE, self.ch)
        elif self.ch == "+":
            tok = Tk(Tk.PLUS, self.ch)
        elif self.ch == "-":
            tok = Tk(Tk.MINUS, self.ch)
        elif self.ch == "/":
            tok = Tk(Tk.SLASH, self.ch)
        elif self.ch == "*":
            tok = Tk(Tk.ASTERISK, self.ch)
        elif self.ch == "<":
            tok = Tk(Tk.LT, self.ch)
        elif self.ch == ">":
            tok = Tk(Tk.GT, self.ch)
        elif self.ch == ";":
            tok = Tk(Tk.SEMICOLON, self.ch)
        elif self.ch == ",":
            tok = Tk(Tk.COMMA, self.ch)
        elif self.ch == "":
            tok = Tk(Tk.EOF, "")
        elif self.ch == "=":
            if self.peek_char() == "=":
                ch = self.ch
                self.read_char()
                tok = Tk(Tk.EQ, ch + self.ch)
            else:
                tok = Tk(Tk.ASSIGN, self.ch)
        elif self.ch == "!":
            if self.peek_char() == "=":
                ch = self.ch
                self.read_char()
                tok = Tk(Tk.NOT_EQ, ch + self.ch)
            else:
                tok = Tk(Tk.BANG, self.ch)
        else:
            if self.is_letter(self.ch):
                literal = self.read_identifier()
                type = tok.lookup_ident(literal)
                return Tk(type, literal)
            elif self.is_digit(self.ch):
                return Tk(Tk.INT, self.read_number())
            else:
                tok = Tk(Tk.ILLEGAL, self.ch)
        self.read_char()
        return tok

    def read_number(self):
        position = self.position
        while self.is_digit(self.ch):
            self.read_char()
        return self.input[position : self.position]

    def read_identifier(self):
        position = self.position
        while self.is_letter(self.ch):
            self.read_char()
        return self.input[position : self.position]

    def is_digit(self, ch):
        return "0" <= ch and ch <= "9"
        # raise Exception("Oi! You need to implement this method!")

    def is_letter(self, ch):
        # return 'a' <= ch && ch <= 'z' || 'A' <= ch && ch <= 'Z' || ch == '_'
        return self.ch.isalpha()

    def peek_char(self):
        if self.read_position > len(self.input):
            return 0
        else:
            return self.input[self.read_position]
