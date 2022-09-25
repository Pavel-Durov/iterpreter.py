from src.kimchi_ast.ast import (
    BlockStatement,
    Boolean,
    CallExpression,
    ExpressionStatement,
    FunctionLiteral,
    Identifier,
    IfExpression,
    InfixExpression,
    IntegerLiteral,
    LetStatement,
    PrefixExpression,
    Program,
    ReturnStatement,
    ArrayLiteral,
    StringLiteral,
    IndexExpression,
    HashLiteral
)

from src.kimchi_tk import Tk
from src.kimchi_trace import trace, untrace


class Parser:
    LOWEST = 0
    EQUALS = 1  # ==
    LESSGREATER = 2  # > or <
    SUM = 3  # +
    PRODUCT = 4  # *
    PREFIX = 5  # -X or !X
    CALL = 6  # myFunction(X)
    INDEX = 8  # [0]

    precedences = {
        Tk.EQ: EQUALS,
        Tk.NOT_EQ: EQUALS,
        Tk.LT: LESSGREATER,
        Tk.GT: LESSGREATER,
        Tk.PLUS: SUM,
        Tk.MINUS: SUM,
        Tk.SLASH: PRODUCT,
        Tk.ASTERISK: PRODUCT,
        Tk.LPAREN: CALL,
        Tk.LBRACKET: INDEX
    }

    def __init__(self, lexer):
        self.l = lexer
        self.cur_token = None
        self.peek_token = None
        self.errors = []

        self.prefixParseFns = {}
        self.reg_prefix(token_type=Tk.IDENT, fn=self.parse_identifier)
        self.reg_prefix(token_type=Tk.INT, fn=self.parse_integer_literal)
        self.reg_prefix(token_type=Tk.BANG, fn=self.parse_prefix_expression)
        self.reg_prefix(token_type=Tk.MINUS, fn=self.parse_prefix_expression)
        self.reg_prefix(token_type=Tk.TRUE, fn=self.parse_boolean)
        self.reg_prefix(token_type=Tk.FALSE, fn=self.parse_boolean)
        self.reg_prefix(token_type=Tk.LPAREN, fn=self.parse_grouped_expression)
        self.reg_prefix(token_type=Tk.IF, fn=self.parse_if_expression)
        self.reg_prefix(token_type=Tk.FUNCTION, fn=self.parse_function_literal)
        self.reg_prefix(token_type=Tk.STRING, fn=self.parse_string_literal)
        self.reg_prefix(token_type=Tk.LBRACKET, fn=self.parse_array_literal)
        self.reg_prefix(token_type=Tk.LBRACE, fn=self.parse_hash_literal)

        self.infixParseFns = {}

        self.reg_infix(token_type=Tk.PLUS, fn=self.parse_infix_expression)
        self.reg_infix(token_type=Tk.MINUS, fn=self.parse_infix_expression)
        self.reg_infix(token_type=Tk.SLASH, fn=self.parse_infix_expression)
        self.reg_infix(token_type=Tk.ASTERISK, fn=self.parse_infix_expression)
        self.reg_infix(token_type=Tk.EQ, fn=self.parse_infix_expression)
        self.reg_infix(token_type=Tk.NOT_EQ, fn=self.parse_infix_expression)
        self.reg_infix(token_type=Tk.LT, fn=self.parse_infix_expression)
        self.reg_infix(token_type=Tk.GT, fn=self.parse_infix_expression)
        self.reg_infix(token_type=Tk.LPAREN, fn=self.parse_call_expression)
        self.reg_infix(token_type=Tk.LBRACKET, fn=self.parse_index_expression)
        # Read two tokens, so cur_token and peek_token are both set
        self.next_token()
        self.next_token()

    def parse_hash_literal(self):
        pairs = {}
        while not self.peek_token_is(Tk.RBRACE):
            self.next_token()
            key = self.parse_expression(self.LOWEST)
            if not self.expect_peek(Tk.COLON):
                return None
            self.next_token()
            value = self.parse_expression(self.LOWEST)
            pairs[key] = value
            if not self.peek_token_is(Tk.RBRACE) and not self.expect_peek(Tk.COMMA):
                return None
        if not self.expect_peek(Tk.RBRACE):
            return None
        return HashLiteral(self.cur_token, pairs)

    def parse_index_expression(self, left):
        self.next_token()
        index = self.parse_expression(self.LOWEST)
        exp = IndexExpression(self.cur_token, left, index)

        if not self.expect_peek(Tk.RBRACKET):
            return None
        return exp

    def parse_array_literal(self):
        return ArrayLiteral(self.cur_token, self.parse_expression_list(Tk.RBRACKET))

    def parse_expression_list(self, end):
        expressions = []
        if self.peek_token_is(end):
            self.next_token()
            return expressions

        self.next_token()

        expressions.append(self.parse_expression(self.LOWEST))

        while self.peek_token_is(Tk.COMMA):
            self.next_token()
            self.next_token()
            expressions.append(self.parse_expression(self.LOWEST))

        if not self.expect_peek(Tk.RBRACKET):
            return None

        return expressions

    def parse_string_literal(self):
        return StringLiteral(self.cur_token, self.cur_token.literal)

    def parse_call_expression(self, func):
        exp = CallExpression(self.cur_token, func, None)
        exp.arguments = self.parse_call_arguments()
        return exp

    def parse_call_arguments(self):
        args = []
        if self.peek_token_is(Tk.RPAREN):
            self.next_token()
            return []
        self.next_token()
        args.append(self.parse_expression(self.LOWEST))

        while self.peek_token_is(Tk.COMMA):
            self.next_token()
            self.next_token()
            args.append(self.parse_expression(self.LOWEST))

        if not self.expect_peek(Tk.RPAREN):
            return None

        return args

    def parse_function_literal(self):
        lit = FunctionLiteral(token=self.cur_token)
        if not self.expect_peek(Tk.LPAREN):
            return None
        lit.parameters = self.parse_function_parameters()
        if not self.expect_peek(Tk.LBRACE):
            return None
        lit.body = self.parse_block_statement()
        return lit

    def parse_function_parameters(self):
        identifiers = []
        if self.peek_token_is(Tk.RPAREN):
            self.next_token()
            return []

        self.next_token()
        ident = Identifier(self.cur_token, self.cur_token.literal)
        identifiers.append(ident)

        while self.peek_token_is(Tk.COMMA):
            self.next_token()
            self.next_token()
            ident = Identifier(self.cur_token, self.cur_token.literal)
            identifiers.append(ident)

        if not self.expect_peek(Tk.RPAREN):
            return None

        return identifiers

    def parse_if_expression(self):
        exp = IfExpression(token=self.cur_token)
        if self.expect_peek(Tk.LPAREN) == False:
            return None
        self.next_token()
        exp.condition = self.parse_expression(self.LOWEST)
        if self.expect_peek(Tk.RPAREN) == False:
            return None
        if self.expect_peek(Tk.LBRACE) == False:
            return None
        exp.consequence = self.parse_block_statement()

        if self.cur_token_is(Tk.ELSE):
            if self.expect_peek(Tk.LBRACE) is False:
                return None
            exp.alternative = self.parse_block_statement()
            # TODO: this might be needed as it diverges from the book
            self.next_token()
        return exp

    def parse_block_statement(self):
        block = BlockStatement(token=self.cur_token)
        self.next_token()
        while (
                self.cur_token_is(Tk.RBRACE) == False and self.cur_token_is(Tk.EOF) == False
        ):
            stmt = self.parse_statement()
            block.statements.append(stmt)
            self.next_token()
        self.next_token()
        return block

    def parse_grouped_expression(self):
        self.next_token()
        exp = self.parse_expression(self.LOWEST)
        if self.expect_peek(Tk.RPAREN) == False:
            return None
        return exp

    def parse_boolean(self):
        return Boolean(self.cur_token, self.cur_token_is(Tk.TRUE))

    def parse_identifier(self):
        return Identifier(self.cur_token, self.cur_token.literal)

    def reg_prefix(self, token_type, fn):
        self.prefixParseFns[token_type] = fn

    def reg_infix(self, token_type, fn):
        self.infixParseFns[token_type] = fn

    def peek_error(self, token_type):
        msg = "expected next token to be {}, got {} instead".format(
            token_type, self.peek_token.type
        )
        self.errors.append(msg)

    def next_token(self):
        self.cur_token = self.peek_token
        self.peek_token = self.l.next_token()

    def parse_program(self):
        prog = Program()
        while self.cur_token.type != Tk.EOF:
            stmt = self.parse_statement()
            if stmt != None:
                prog.statements.append(stmt)
            self.next_token()
        return prog

    def parse_infix_expression(self, left):
        trace("parse_infix_expression:start")
        exp = InfixExpression(
            token=self.cur_token, operator=self.cur_token.literal, left=left
        )
        precedence = self.cur_precedence()
        self.next_token()
        exp.right = self.parse_expression(precedence)
        untrace("parse_infix_expression:end")
        return exp

    def parse_prefix_expression(self):
        trace("parse_prefix_expression:start")
        exp = PrefixExpression(token=self.cur_token, operator=self.cur_token.literal)
        self.next_token()
        exp.right = self.parse_expression(self.PREFIX)
        untrace("parse_prefix_expression:end")
        return exp

    def parse_let_statement(self):
        trace("parse_let_statement:start")
        stmt = LetStatement(token=self.cur_token, identifier=None, value_exp=None)
        if not self.expect_peek(Tk.IDENT):
            return None

        stmt.name = Identifier(self.cur_token, self.cur_token.literal)
        if not self.expect_peek(Tk.ASSIGN):
            return None
        self.next_token()

        stmt.value = self.parse_expression(self.LOWEST)

        while not self.cur_token_is(Tk.SEMICOLON):
            self.next_token()
        untrace("parse_let_statement:end")
        return stmt

    def parse_return_statement(self):
        trace("parse_return_statement:start")
        stmt = ReturnStatement(token=self.cur_token, return_value=None)
        self.next_token()
        stmt.return_value = self.parse_expression(self.LOWEST)
        while not self.cur_token_is(Tk.SEMICOLON):
            self.next_token()
        untrace("parse_return_statement:end")
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
        trace("parse_expression:start")
        prefix = self.prefixParseFns[self.cur_token.type]
        if prefix == None:
            self.on_prefix_parse_fn_error(self.cur_token.type)
            return None
        left_exp = prefix()
        while (self.peek_token_is(Tk.SEMICOLON) == False and precedence < self.peek_precedence()):
            infix = self.infixParseFns[self.peek_token.type]
            if infix == None:
                return left_exp
            self.next_token()
            left_exp = infix(left_exp)
        untrace("parse_expression:end")
        return left_exp

    def parse_integer_literal(self):
        trace("parse_integer_literal:start")
        value = 0
        try:
            value = int(self.cur_token.literal)
        except ValueError:
            self.errors.append(
                "could not parse {} as integer".format(self.cur_token.literal)
            )
            return None
        untrace("parse_integer_literal:end")
        return IntegerLiteral(self.cur_token, value)

    def parse_expression_statement(self):
        trace("parse_expression_statement:start")
        exp = self.parse_expression(self.LOWEST)
        stms = ExpressionStatement(token=self.cur_token, expression=exp)
        if self.peek_token_is(Tk.SEMICOLON):
            self.next_token()
        untrace("parse_expression_statement:end")
        return stms

    def parse_statement(self):
        if self.cur_token.type == Tk.LET:
            return self.parse_let_statement()
        elif self.cur_token.type == Tk.RETURN:
            return self.parse_return_statement()
        else:
            return self.parse_expression_statement()

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
