from src.kimchi_ast.ast import ExpressionStatement, IntegerLiteral, Program, Boolean
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
  if isinstance(node, Boolean):
    return native_bool_to_boolean_object(node.value)
  
  return None

def eval_statements(statements):
  result = None

  for statement in statements:
    result = eval(statement)

  return result

def native_bool_to_boolean_object(input):
  if input:
    return TRUE
  return FALSE