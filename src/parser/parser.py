from distutils.sysconfig import PREFIX
from src.ast.ast import ExpressionStatement, Identifier, InfixExpression, IntegerLiteral, LetStatement, PrefixExpression, Program, ReturnStatement
from src.token import Token
from src.trace import trace, untrace


class Parser():

    LOWEST = 0
    EQUALS = 1  # == 
    LESSGREATER = 2 # > or <
    SUM = 3 # +
    PRODUCT = 4  # *
    PREFIX = 5 # -X or !X
    CALL = 6 # myFunction(X)
    
    precedences = { 
      Token.EQ: EQUALS,
      Token.NOT_EQ: EQUALS,
      Token.LT: LESSGREATER,
      Token.GT: LESSGREATER,
      Token.PLUS: SUM,
      Token.MINUS: SUM,
      Token.SLASH: PRODUCT,
      Token.ASTERISK: PRODUCT,
  }
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
        self.reg_infix(token_type=Token.PLUS, fn=self.parse_infix_expression)
        self.reg_infix(token_type=Token.MINUS, fn=self.parse_infix_expression)
        self.reg_infix(token_type=Token.SLASH, fn=self.parse_infix_expression)
        self.reg_infix(token_type=Token.ASTERISK, fn=self.parse_infix_expression)
        self.reg_infix(token_type=Token.EQ, fn=self.parse_infix_expression)
        self.reg_infix(token_type=Token.NOT_EQ, fn=self.parse_infix_expression)
        self.reg_infix(token_type=Token.LT, fn=self.parse_infix_expression)
        self.reg_infix(token_type=Token.GT, fn=self.parse_infix_expression)
        
        
        
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
    
    def parse_infix_expression(self, left):
        trace('parse_infix_expression:start')  
        exp = InfixExpression(token=self.cur_token, operator=self.cur_token.literal, left=left)
        precedence = self.cur_precedence()
        self.next_token()
        exp.right = self.parse_expression(precedence)
        untrace('parse_infix_expression:end')  
        return exp

    def parse_prefix_expression(self):
        trace('parse_prefix_expression:start')
        exp = PrefixExpression(token=self.cur_token, operator=self.cur_token.literal)
        self.next_token()
        exp.right = self.parse_expression(PREFIX)
        untrace('parse_prefix_expression:end')
        return exp
    
    
    def parse_let_statement(self):
        trace('parse_let_statement:start')  
        stmt = LetStatement(token=self.cur_token, identifier=None, value_exp=None)
        if self.expect_peek(Token.IDENT) == False:
            return None
        
        stmt.name = Identifier(self.cur_token, self.cur_token.literal)
        if self.expect_peek(Token.ASSIGN) == False:
            return None
        
        # TODO: We're skipping the expressions until we encounter a semicolon
        while self.cur_token_is(Token.SEMICOLON) == False:
            self.next_token()
        untrace('parse_let_statement:end')  
        return stmt
        
    def parse_return_statement(self):
        trace('parse_return_statement:start')  
        stmt = ReturnStatement(token=self.cur_token, return_value=None)
        self.next_token()
        # TODO: We're skipping the expressions until we encounter a semicolon
        while self.cur_token_is(Token.SEMICOLON) == False:
            self.next_token()
        untrace('parse_return_statement:end')  
        return stmt
    
    def on_prefix_parse_fn_error(self, token_type):
        self.errors.append("no prefix parse function for {} found".format(token_type))

    def peek_precedence(self):
        if self.peek_token.type in self.precedences:
            return self.precedences[self.peek_token.type]
        return self.LOWEST

    def cur_precedence(self):
        if self.cur_token.type in self.precedences:
            return self.precedences[self.cur_token.type]
        return self.LOWEST

    def parse_expression(self, precedence):
        trace('parse_expression:start')
        prefix = self.prefixParseFns[self.cur_token.type]
        if prefix == None:
            self.on_prefix_parse_fn_error(self.cur_token.type)
            return None
        left_exp = prefix()
        while self.peek_token_is(Token.SEMICOLON) == False and precedence < self.peek_precedence():
            infix = self.infixParseFns[self.peek_token.type]
            if infix == None:
                return left_exp
            self.next_token()
            left_exp = infix(left_exp)
        untrace('parse_expression:end')
        return left_exp      


    def parse_integer_literal(self):
        trace('parse_integer_literal:start')
        value = 0
        try:
          value = int(self.cur_token.literal)
        except ValueError:
          self.errors.append("could not parse {} as integer".format(self.cur_token.literal))
          return None
        untrace('parse_integer_literal:end')
        return IntegerLiteral(self.cur_token, value)

        

    def parse_expression_statement(self):
        trace('parse_expression_statement:start')
        stms = ExpressionStatement(token=self.cur_token, expression=self.parse_expression(self.LOWEST))
        if self.peek_token_is(Token.SEMICOLON):
            self.next_token()
        untrace('parse_expression_statement:end')
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
