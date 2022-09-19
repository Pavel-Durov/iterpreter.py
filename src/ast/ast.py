
from src.token import Token

class Node():
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


### Let statement

class LetStatement(Node):
    def __init__(self, token, identifier, value_exp):
        self.token = token # Token.LET
        self.name = identifier # Identifier
        self.value = value_exp # Expression

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

## Identifier

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

## Returns  

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
        return self.token_literal()+ " " +self.return_value + ";"


## Expressions
class ExpressionStatement(Statement):
    def __init__(self, token, expression):
        self.token = token # the first token of the expression
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

# Literals
class IntegerLiteral(Expression):
    def __init__(self, token, value):
        self.token = token
        self.value = value


    def expression_node(self):
        pass


    def token_literal(self):
        return self.token.literal


    def __str__(self):
        return self.token.literal    

# PrefixExpression
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
    def __init__(self, token, left, operator):
        self.token = token
        self.left = left
        self.operator = operator

    def expression_node(self):
        pass


    def token_literal(self):
        return self.token.literal       

    def __str__(self):
        return "(" + str(self.left) + " " + self.operator + " " + str(self.right) + ")"


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