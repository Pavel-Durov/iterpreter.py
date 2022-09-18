

from src.ast.ast import Identifier, LetStatement, Program
from src.token import Token

class Parser():
    def __init__(self, lexer):
        self.l = lexer
        self.cur_token = None
        self.peek_token = None
        self.errors = []
        
        # Read two tokens, so curToken and peekToken are both set
        self.next_token()
        self.next_token()

    def peek_error(self, token_type):
        msg = "expected next token to be {}, got {} instead".format(token_type, self.peek_token.type)
        self.errors.append(msg)


    def next_token(self):
        self.cur_token = self.peek_token
        self.peek_token = self.l.next_token()


    def parse_program(self):
        prog = Program()
        while self.cur_token.type != Token.EOF:
            stmt = self.parse_statement()
            if stmt != None:
                prog.statements.append(stmt)
                print("@@@", prog.statements)
            self.next_token()
        return prog

    def parse_let_statement(self):
        stmt = LetStatement(token=self.cur_token, identifier=None, value_exp=None)
        if self.expect_peek(Token.IDENT) == False:
            return None
        
        stmt.name = Identifier(self.cur_token, self.cur_token.literal)
        if self.expect_peek(Token.ASSIGN) == False:
            return None
        

        # TODO: We're skipping the expressions until we encounter a semicolon
        while self.cur_token_is(Token.SEMICOLON) == False:
            self.next_token()
        
        return stmt

    def cur_token_is(self, token_type):
        return self.cur_token.type == token_type

    def peek_token_is(self, token_type):
        return self.peek_token.type == token_type

    def expect_peek(self, token_type):
        if self.peek_token_is(token_type):
            self.next_token()
            return True
        else:
            self.peek_error(token_type)
            return False

    def parse_statement(self):
        if self.cur_token.type == Token.LET:
            return self.parse_let_statement()
        return None


