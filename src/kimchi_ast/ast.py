class Node:
    def __init__(self):
        pass

    def token_literal():
        pass


class Statement(Node):
    def token_literal():
        pass


class Expression(Node):
    def token_literal():
        pass

    def expression_node():
        pass


class Program(Node):
    def __init__(self):
        self.statements = []

    def token_literal(self):
        if len(self.statements) > 0:
            return self.statements[0].token_literal()
        return ""

    def __str__(self):
        out = ""
        for s in self.statements:
            out += str(s)
        return out


class LetStatement(Node):
    def __init__(self, token, identifier, value_exp):
        self.token = token  # Token.LET
        self.name = identifier  # Identifier
        self.value = value_exp  # Expression

    def token_literal(self):
        return self.token.literal

    def __str__(self):
        out = self.token_literal() + " " + self.name.value + " = "
        if self.value != None:
            out += str(self.value)
        out += ";"
        return out

    def statement_node(self):
        pass


class AssignStatement(Node):
    def __init__(self, token, identifier, value_exp):
        self.token = token  # Token.LET
        self.name = identifier  # Identifier
        self.value = value_exp  # Expression

    def token_literal(self):
        return self.token.literal

    def __str__(self):
        out = self.token_literal() + " " + self.name.value + " = "
        if self.value != None:
            out += str(self.value)
        out += ";"
        return out

    def statement_node(self):
        pass


class Identifier(Expression):
    def __init__(self, token, value):
        self.token = token
        self.value = value

    def expression_node(self):
        pass

    def token_literal(self):
        return self.token.literal

    def __str__(self):
        return self.value


class ReturnStatement(Statement):
    def __init__(self, token, return_value):
        self.token = token
        self.return_value = return_value

    def token_literal(self):
        return self.token.literal

    def __str__(self):
        out = self.token_literal() + " "
        if self.return_value != None:
            out += str(self.return_value)
        out += ";"
        return out

    def statement_node(self):
        pass

    def __str__(self):
        return self.token_literal() + " " + self.return_value + ";"


class ExpressionStatement(Statement):
    def __init__(self, token, expression):
        self.token = token  # the first token of the expression
        self.expression = expression

    def token_literal(self):
        return self.token.literal

    def __str__(self):
        if self.expression != None:
            return str(self.expression)
        return ""

    def statement_node(self):
        pass

    def __str__(self):
        if self.expression is not None:
            return str(self.expression)
        return ""


class IntegerLiteral(Expression):
    def __init__(self, token, value):
        self.token = token
        self.value = value
        self.int_value = value

    def expression_node(self):
        pass

    def token_literal(self):
        return self.token.literal

    def __str__(self):
        return self.token.literal


class PrefixExpression(Expression):
    def __init__(self, token, operator, right=None):
        self.token = token
        assert operator in ["!", "-"]
        self.operator = operator
        self.right = right

    def expression_node(self):
        pass

    def token_literal(self):
        return self.token.literal

    def __str__(self):
        return "(" + self.operator + str(self.right) + ")"


class InfixExpression(Expression):
    ASSIGN = 0  # "="
    PLUS = 1  # "+"
    MINUS = 2  # "-"
    BANG = 3  # "!"
    MUL = 4  # "*"
    DIV = 5  # "/"
    LT = 6  # "<"
    GT = 7  # ">"
    EQ = 8  # "=="
    NOT_EQ = 9  # "!="

    op_to_code = {
        "=": ASSIGN,
        "+": PLUS,
        "-": MINUS,
        "!": BANG,
        "*": MUL,
        "/": DIV,
        "<": LT,
        ">": GT,
        "==": EQ,
        "!=": NOT_EQ,
    }

    def __init__(self, token, left, operator):
        self.token = token
        self.left = left
        self.literal_operator = operator
        assert operator in self.op_to_code, 'expected one of: ' + str(self.op_to_code.keys()) + 'got: ' + operator
        self.operator = self.op_to_code[operator]

    def expression_node(self):
        pass

    def token_literal(self):
        return self.token.literal

    def __str__(self):
        return "(" + str(self.left) + " " + self.literal_operator + " " + str(self.right) + ")"


class Boolean(Expression):
    def __init__(self, token, value):
        self.token = token
        self.value = value

    def expression_node(self):
        pass

    def token_literal(self):
        return self.token.literal

    def __str__(self):
        return self.token.literal


class IfExpression(Expression):
    def __init__(self, token=None, condition=None, consequence=None, alternative=None):
        self.token = token
        self.condition = condition
        self.consequence = consequence  # BlockStatement
        self.alternative = alternative  # BlockStatement

    def expression_node(self):
        pass

    def token_literal(self):
        return self.token.literal

    def __str__(self):
        out = "if" + str(self.condition) + " " + str(self.consequence)
        if self.alternative != None:
            out += "else " + str(self.alternative)
        return out


class BlockStatement(Statement):
    def __init__(self, token):
        self.token = token
        self.statements = []

    def token_literal(self):
        return self.token.literal

    def statement_node(self):
        pass

    def __str__(self):
        out = ""
        for s in self.statements:
            out += str(s)
        return out


class FunctionLiteral(Expression):
    def __init__(self, token, parameters=None, body=None):
        self.token = token
        self.parameters = parameters
        self.body = body

    def expression_node(self):
        pass

    def token_literal(self):
        return self.token.literal

    def __str__(self):
        params = []
        for p in self.parameters:
            params.append(str(p))
        return self.token_literal() + "(" + ", ".join(params) + ") " + str(self.body)


class CallExpression(Expression):
    def __init__(self, token, function, arguments):
        self.token = token
        self.function = function
        self.arguments = arguments

    def expression_node(self):
        pass

    def token_literal(self):
        return self.token.literal

    def __str__(self):
        args = []
        for a in self.arguments:
            args.append(str(a))
        return str(self.function) + "(" + ", ".join(args) + ")"


class StringLiteral(Expression):
    def __init__(self, token, value):
        self.token = token
        self.value = value

    def expression_node(self):
        pass

    def token_literal(self):
        return self.token.literal

    def __str__(self):
        return self.token.literal


class IndexExpression(Expression):
    def __init__(self, token, left, index):
        self.token = token
        self.left = left
        self.index = index

    def expression_node(self):
        pass

    def token_literal(self):
        return self.token.literal

    def __str__(self):
        return "(" + str(self.left) + "[" + str(self.index) + "])"


class ArrayLiteral(Expression):
    def __init__(self, token, elements):
        self.token = token
        self.elements = elements

    def expression_node(self):
        pass

    def token_literal(self):
        return self.token.literal

    def __str__(self):
        elements = []
        for e in self.elements:
            elements.append(str(e))
        return "[" + ", ".join(elements) + "]"


class HashLiteral(Expression):
    def __init__(self, token, pairs):
        self.token = token
        self.pairs = pairs

    def expression_node(self):
        pass

    def token_literal(self):
        return self.token.literal

    def __str__(self):
        pairs = []
        for key, value in self.pairs.items():
            pairs.append(str(key) + ":" + str(value))
        return "{" + ", ".join(pairs) + "}"


class WhileExpression(Expression):
    def __init__(self, token=None, condition=None, block=None):
        self.token = token
        self.condition = condition
        self.body = block

    def expression_node(self):
        pass

    def token_literal(self):
        return self.token.literal

    def __str__(self):
        out = "while" + str(self.condition) + " " + str(self.consequence)
        if self.body != None:
            out += "else " + str(self.body)
        return out
