from src.kimchi_ast.ast import ExpressionStatement, InfixExpression, IntegerLiteral, PrefixExpression, Program, Boolean
import src.kimchi_object.object as obj

TRUE = obj.Boolean(True)
FALSE = obj.Boolean(False)
NULL = obj.Null()

def eval(node):
    # statements
    if isinstance(node, Program):
      return eval_statements(node.statements)

    if isinstance(node, ExpressionStatement):
      return eval(node.expression) 

    # expressions
    if isinstance(node, IntegerLiteral):
      return obj.Integer(node.value)
    elif isinstance(node, Boolean):
      return native_bool_to_boolean_object(node.value)
    elif isinstance(node, PrefixExpression):
      right = eval(node.right)
      return eval_prefix_expression(node.operator, right)
    elif isinstance(node, InfixExpression):
      left = eval(node.left)
      right = eval(node.right)
      return eval_infix_expression(node.operator, left, right)
    return None

def eval_integer_infix_expression(operator, left, right):
    left_val = left.value
    right_val = right.value
    if operator == "+":
      return obj.Integer(left_val + right_val)
    elif operator == "-":
      return obj.Integer(left_val - right_val)
    elif operator == "*":
      return obj.Integer(left_val * right_val)
    elif operator == "/":
      return obj.Integer(left_val / right_val)
    elif operator == "<":
      return native_bool_to_boolean_object(left_val < right_val)
    elif operator == ">":
      return native_bool_to_boolean_object(left_val > right_val)
    elif operator == "==":
      return native_bool_to_boolean_object(left_val == right_val)
    elif operator == "!=":
      return native_bool_to_boolean_object(left_val != right_val)
    return NULL


def eval_infix_expression(operator, left, right):
    if isinstance(left, obj.Integer) and isinstance(right, obj.Integer):
      return eval_integer_infix_expression(operator, left, right)
    elif operator == "==":
      return native_bool_to_boolean_object(left == right)
    elif operator == "!=":
      return native_bool_to_boolean_object(left != right)
    return NULL


def eval_bang_operator_expression(right):
    if right == TRUE:
      return FALSE
    if right == FALSE:
      return TRUE
    if right == NULL:
      return TRUE
    return FALSE


def eval_minus_prefix_operator_expression(right):
    if isinstance(right, obj.Integer):
      value = right.value
      return obj.Integer(-value)
    return NULL

def eval_prefix_expression(operator, right):
    if operator == "!":
      return eval_bang_operator_expression(right)
    elif operator == "-":
      return eval_minus_prefix_operator_expression(right)
    return NULL


def eval_statements(statements):
    result = None

    for statement in statements:
      result = eval(statement)

    return result


def native_bool_to_boolean_object(input):
    if input:
      return TRUE
    return FALSE