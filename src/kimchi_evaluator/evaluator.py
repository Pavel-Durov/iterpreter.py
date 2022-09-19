import src.kimchi_object.object as obj
from src.kimchi_object import Environment

from src.kimchi_ast.ast import BlockStatement, ExpressionStatement, FunctionLiteral, Identifier, IfExpression, InfixExpression, \
    IntegerLiteral, LetStatement, PrefixExpression, Program, Boolean, ReturnStatement, CallExpression
TRUE = obj.Boolean(True)
FALSE = obj.Boolean(False)
NULL = obj.Null()


def eval(node, env):
    if isinstance(node, Program):
        return eval_program(node, env)
    elif isinstance(node, ExpressionStatement):
        return eval(node.expression, env)
    elif isinstance(node, ReturnStatement):
        val = eval(node.return_value, env)
        if isinstance(val, obj.Error):
            return val
        return obj.ReturnValue(val)
    elif isinstance(node, BlockStatement):
        return eval_block_statement(node, env)
    elif isinstance(node, CallExpression):
        func = eval(node.function, env)
        if isinstance(func, obj.Error):
            return func
        args = eval_expressions(node.arguments, env)
        if len(args) == 1 and isinstance(args[0], obj.Error):
            return args[0]
        return apply_function(func, args)
    elif isinstance(node, FunctionLiteral):
        return obj.Function(node.parameters, node.body, env)
    elif isinstance(node, IntegerLiteral):
        return obj.Integer(node.value)
    elif isinstance(node, LetStatement):
        val = eval(node.value, env)
        if isinstance(val, obj.Error):
            return val
        env.set(node.name.value, val)
    elif isinstance(node, Identifier):
        return eval_identifier(node, env)
    elif isinstance(node, Boolean):
        return native_bool_to_boolean_object(node.value)
    elif isinstance(node, PrefixExpression):
        right = eval(node.right, env)
        if isinstance(right, obj.Error):
            return right
        return eval_prefix_expression(node.operator, right)
    elif isinstance(node, InfixExpression):
        left = eval(node.left, env)
        if isinstance(left, obj.Error):
            return left
        right = eval(node.right, env)
        if isinstance(right, obj.Error):
            return right
        return eval_infix_expression(node.operator, left, right)

    elif isinstance(node, IfExpression):
        return eval_if_expression(node, env)

    return None

def unwrap_return_value(wrapper):
    if isinstance(wrapper, obj.ReturnValue):
        return wrapper.value
    return wrapper

def extend_function_env(fn, args):
  env = Environment(fn.env)
  
  for param_idx, param in enumerate(fn.parameters):
      env.set(param.value, args[param_idx])
  
  return env
  
def apply_function(fn, args):
  assert isinstance(fn, obj.Function), "fn must be a Function, got %s" % type(fn)
  extended_env = extend_function_env(fn, args)
  evaluated = eval(fn.body, extended_env)
  return unwrap_return_value(evaluated)


def eval_expressions(args, env):
  result = []
  for arg in args:
      evaluated = eval(arg, env)
      if isinstance(evaluated, obj.Error):
          return [evaluated]
      result.append(evaluated)
  return result


def eval_identifier(node, env):
    val = env.get(node.value)
    if not val:
        return obj.Error("identifier not found: {}".format(node.value))
    return val


def eval_block_statement(block, env):
    result = None
    for statement in block.statements:
        result = eval(statement, env)
        if result is not None:
            if isinstance(result, obj.ReturnValue) or isinstance(result, obj.Error):
                return result
    return result


def eval_program(prog, env):
    result = None

    for statement in prog.statements:
        result = eval(statement, env)
        if isinstance(result, obj.ReturnValue):
            return result.value
        elif isinstance(result, obj.Error):
            return result

    return result


def is_truthy(obj):
    if obj == NULL:
        return False
    if obj == TRUE:
        return True
    if obj == FALSE:
        return False
    return True


def eval_if_expression(node, env):
    condition = eval(node.condition, env)
    if isinstance(condition, obj.Error):
        return condition
    if is_truthy(condition):
        return eval(node.consequence, env)
    elif node.alternative is not None:
        return eval(node.alternative, env)
    return NULL


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
    return obj.Error("unknown operator: {} {} {}".format(left.type(), operator, right.type))


def eval_infix_expression(operator, left, right):
    if isinstance(left, obj.Integer) and isinstance(right, obj.Integer):
        return eval_integer_infix_expression(operator, left, right)
    elif operator == "==":
        return native_bool_to_boolean_object(left == right)
    elif operator == "!=":
        return native_bool_to_boolean_object(left != right)
    elif left.type() != right.type():
        return obj.Error("type mismatch: {} {} {}".format(left.type(), operator, right.type()))
    return obj.Error("unknown operator: {} {} {}".format(left.type(), operator, right.type()))


def eval_bang_operator_expression(right):
    if right == TRUE:
        return FALSE
    if right == FALSE:
        return TRUE
    if right == NULL:
        return TRUE
    return FALSE


def eval_minus_prefix_operator_expression(right):
    if not isinstance(right, obj.Integer):
        return obj.Error("unknown operator: -{}".format(right.type()))
    return obj.Integer(-right.value)


def eval_prefix_expression(operator, right):
    if operator == "!":
        return eval_bang_operator_expression(right)
    elif operator == "-":
        return eval_minus_prefix_operator_expression(right)
    return obj.Error("unknown operator: {}{}".format(operator, right.type()))


def native_bool_to_boolean_object(input):
    if input:
        return TRUE
    return FALSE
