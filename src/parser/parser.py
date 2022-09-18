

from src.ast.ast import ExpressionStatement, Identifier, IntegerLiteral, LetStatement, PrefixExpression, Program, ReturnStatement
from src.token import Token

class Parser():

    LOWEST = 0
    EQUALS = 1  # == 
    LESSGREATER = 2 # > or <
    SUM = 3 # +
    PRODUCT = 4  # *
    PREFIX = 5 # -Xor!X
    CALL = 6 # myFunction(X)
    
    def __init__(self, lexer):
        self.l = lexer
        self.cur_token = None
        self.peek_token = None
        self.errors = []

        self.prefixParseFns = {}
        self.reg_prefix(token_type=Token.IDENT, fn=self.parse_identifier)
        self.reg_prefix(token_type=Token.INT, fn=self.parse_integer_literal)
        self.reg_prefix(token_type=Token.BANG, fn=self.parse_prefix_expression)
        self.reg_prefix(token_type=Token.MINUS, fn=self.parse_prefix_expression)
        self.infixParseFns = {}
        
        
        # Read two tokens, so curToken and peekToken are both set
        self.next_token()
        self.next_token()


    def parse_identifier(self):
      return Identifier(self.cur_token, self.cur_token.literal)


    def reg_prefix(self, token_type, fn):
        self.prefixParseFns[token_type] = fn
    
    def reg_infix(self, token_type, fn):
        self.infixParseFns[token_type] = fn

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
            self.next_token()
        return prog
    
    
    def parse_prefix_expression(self):
        exp = PrefixExpression(token=self.cur_token, operator=self.cur_token.literal, right=None)
        self.next_token()
        exp.right = self.parse_expression(self.PREFIX)
        return exp
    
    
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
        
    def parse_return_statement(self):
        stmt = ReturnStatement(token=self.cur_token, return_value=None)
        self.next_token()
        # TODO: We're skipping the expressions until we encounter a semicolon
        while self.cur_token_is(Token.SEMICOLON) == False:
            self.next_token()
        return stmt
    
    def on_prefix_parse_fn_error(self, token_type):
        self.errors.append("no prefix parse function for {} found".format(token_type))

    def parse_expression(self, precedence):
        prefix = self.prefixParseFns[self.cur_token.type]
        if prefix == None:
            self.on_prefix_parse_fn_error(self.cur_token.type)
            return None
        left_exp = prefix()
        # while self.peek_token_is(Token.SEMICOLON) == False and precedence < self.peekPrecedence():
        #     infix = self.infixParseFns[self.peek_token.type]
        #     if infix == None:
        #         return left_exp
        #     self.next_token()
        #     left_exp = infix(left_exp)
        return left_exp      


    def parse_integer_literal(self):
        value = 0
        try:
          value = int(self.cur_token.literal)
        except ValueError:
          self.errors.append("could not parse {} as integer".format(self.cur_token.literal))
          return None
        return IntegerLiteral(self.cur_token, value)

        

    def parse_expression_statement(self):
        stms = ExpressionStatement(token=self.cur_token, expression= self.parse_expression(self.LOWEST))
        if self.peek_token_is(Token.SEMICOLON):
            self.next_token()
        return stms

    def parse_statement(self):
        if self.cur_token.type == Token.LET:
            return self.parse_let_statement()
        elif self.cur_token.type == Token.RETURN:
            return self.parse_return_statement()
        else:
            return self.parse_expression_statement()
        return None
    

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
