import src.kimchi_ast as ast
import src.kimchi_object as obj
from src.kimchi_evaluator.const import TRUE, FALSE, NULL
from src.kimchi_io import print_line

builtins = {
    "len": True,
    "first": True,
    "last": True,
    "rest": True,
    "push": True,
    "puts": True,
}


def eval(node, env):
    if isinstance(node, ast.Program):
        return eval_program(node, env)
    elif isinstance(node, ast.HashLiteral):
        return eval_hash_literal(node, env)
    elif isinstance(node, ast.IndexExpression):
        left = eval(node.left, env)
        if isinstance(left, obj.Error):
            return left
        index = eval(node.index, env)
        if isinstance(index, obj.Error):
            return index
        return eval_index_expression(left, index)
    elif isinstance(node, ast.StringLiteral):
        return obj.String(node.value)
    elif isinstance(node, ast.ArrayLiteral):
        elements = eval_expressions(node.elements, env)
        if len(elements) == 1 and isinstance(elements[0], obj.Error):
            return elements[0]
        return obj.Array(elements)
    elif isinstance(node, ast.ExpressionStatement):
        return eval(node.expression, env)
    elif isinstance(node, ast.ReturnStatement):
        val = eval(node.return_value, env)
        if isinstance(val, obj.Error):
            return val
        return obj.ReturnValue(val)
    elif isinstance(node, ast.BlockStatement):
        return eval_block_statement(node, env)
    elif isinstance(node, ast.CallExpression):
        func = eval(node.function, env)
        if isinstance(func, obj.Error):
            return func
        args = eval_expressions(node.arguments, env)
        if len(args) == 1 and isinstance(args[0], obj.Error):
            return args[0]
        return apply_function(func, args)
    elif isinstance(node, ast.FunctionLiteral):
        return obj.Function(node.parameters, node.body, env)
    elif isinstance(node, ast.IntegerLiteral):
        return obj.Integer(node.value)
    elif isinstance(node, ast.LetStatement):
        val = eval(node.value, env)
        if isinstance(val, obj.Error):
            return val
        env.set(node.name.value, val)
    elif isinstance(node, ast.Identifier):
        return eval_identifier(node, env)
    elif isinstance(node, ast.Boolean):
        return native_bool_to_boolean_object(node.value)
    elif isinstance(node, ast.PrefixExpression):
        right = eval(node.right, env)
        if isinstance(right, obj.Error):
            return right
        return eval_prefix_expression(node.operator, right)
    elif isinstance(node, ast.InfixExpression):
        left = eval(node.left, env)
        if isinstance(left, obj.Error):
            return left
        right = eval(node.right, env)
        if isinstance(right, obj.Error):
            return right
        return eval_infix_expression(node.operator, left, right)

    elif isinstance(node, ast.IfExpression):
        return eval_if_expression(node, env)

    return None


def eval_hash_literal(node, env):
    pairs = {}

    for key_node, value_node in node.pairs.items():
        key = eval(key_node, env)
        if isinstance(key, obj.Error):
            return key
        value = eval(value_node, env)
        if isinstance(value, obj.Error):
            return value
        if isinstance(value, obj.HashableObject):
            hashed = key.hash_key()
            pairs[hashed] = obj.HashPair(key, value)

    return obj.Hash(pairs)


def eval_hash_index_expression(hash, index):
    if not isinstance(index, obj.HashableObject):
        return obj.Error("unusable as hash key: %s" % (index.type()))
    pair = hash.pairs.get(index.hash_key())
    if pair:
        return pair.value
    return NULL


def eval_index_expression(left, index):
    if isinstance(left, obj.Array) and isinstance(index, obj.Integer):
        return eval_array_index_expression(left, index)
    elif isinstance(left, obj.Hash):
        return eval_hash_index_expression(left, index)
    return obj.Error("index operator not supported: %s" % (left.type()))


def eval_array_index_expression(array, index):
    idx = index.value
    max = len(array.elements) - 1
    if idx < 0 or idx > max:
        return NULL
    return array.elements[idx]


def unwrap_return_value(wrapper):
    if isinstance(wrapper, obj.ReturnValue):
        return wrapper.value
    return wrapper


def extend_function_env(fn, args):
    env = obj.Environment(fn.env)

    for param_idx, param in enumerate(fn.parameters):
        env.set(param.value, args[param_idx])

    return env


def apply_function(fn, args):
    if isinstance(fn, obj.Function):
        extended_env = extend_function_env(fn, args)
        evaluated = eval(fn.body, extended_env)
        return unwrap_return_value(evaluated)
    if args is None:
        return None
    if fn.name == "len":
        if isinstance(args, list) and len(args) == 1:
            return builtin_len(args[0])
        else:
            return obj.Error("wrong number of arguments. got=%d, want=1" % (len(args)))
    elif fn.name == "puts":
        return builtin_puts(args)
    elif fn.name == "first":
        return builtin_first(args)
    elif fn.name == "last":
        return builtin_last(args)
    elif fn.name == "rest":
        return builtin_rest(args)
    elif fn.name == "push":
        return builtin_push(args)
    return obj.Error("not a function: %s" % (fn.type()))


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
    if val:
        return val
    if node.value in builtins:
        return obj.Builtin(node.value)
    return obj.Error("identifier not found: %s" % (node.value))


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

    return obj.Error("unknown operator: %s %s %s" % (str(left.type()), str(operator), str(right.type())))


def eval_infix_expression(operator, left, right):
    if isinstance(left, obj.Integer) and isinstance(right, obj.Integer):
        return eval_integer_infix_expression(operator, left, right)
    elif operator == "==":
        return native_bool_to_boolean_object(left == right)
    elif operator == "!=":
        return native_bool_to_boolean_object(left != right)
    elif isinstance(left, obj.String) and isinstance(right, obj.String):
        return eval_string_infix_expression(left, right, operator)
    elif left.type() != right.type():
        return obj.Error("type mismatch: %s %s %s" % (left.type(), operator, right.type()))
    return obj.Error("unknown operator: %s %s %s" % (left.type(), operator, right.type()))


def eval_string_infix_expression(left, right, operator):
    if operator != "+":
        return obj.Error("Unknown operator: %s %s %s" % (left.type(), operator, right.type()))
    return obj.String(left.value + right.value)


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
        return obj.Integer(-right.value)

    return obj.Error("unknown operator: -%s" % (right.type()))


def eval_prefix_expression(operator, right):
    if operator == "!":
        return eval_bang_operator_expression(right)
    elif operator == "-":
        return eval_minus_prefix_operator_expression(right)
    return obj.Error("unknown operator: %s" % (operator, right.type()))


def native_bool_to_boolean_object(input):
    if input:
        return TRUE
    return FALSE


def builtin_len(arg):
    if isinstance(arg, obj.String):
        return obj.Integer(len(arg.value))
    elif isinstance(arg, obj.Array):
        return obj.Integer(len(arg.elements))
    else:
        return obj.Error("argument to `len` not supported, got %s" % (arg.type()))


def builtin_first(args):
    if len(args) != 1:
        return obj.Error("wrong number of arguments. got=%d, want=1" % (len(args)))
    arg = args[0]
    if not isinstance(arg, obj.Array):
        return obj.Error("argument to `first` must be ARRAY, got %s" % (arg.type()))
    if len(arg.elements) > 0:
        return arg.elements[0]
    else:
        return NULL


def builtin_last(args):
    if len(args) != 1:
        return obj.Error("wrong number of arguments. got=%d, want=1" % (len(args)))
    arg = args[0]
    if not isinstance(arg, obj.Array):
        return obj.Error("argument to `last` must be ARRAY, got %s" % (arg.type()))
    if len(arg.elements) > 0:
        return arg.elements[-1]
    else:
        return NULL


def builtin_rest(args):
    if len(args) != 1:
        return obj.Error("wrong number of arguments. got=%d, want=1" % (len(args)))
    arg = args[0]
    if not isinstance(arg, obj.Array):
        return obj.Error("argument to `rest` must be ARRAY, got %s" % (arg.type()))
    if len(arg.elements) > 0:
        return obj.Array(arg.elements[1:])
    else:
        return NULL


def builtin_push(args):
    if len(args) != 2:
        return obj.Error("wrong number of arguments. got=%d, want=2" % len(args))
    arg = args[0]
    if not isinstance(arg, obj.Array):
        return obj.Error("argument to `push` must be ARRAY, got %s" % (arg.type()))
    new_element = args[1]
    new_elements = arg.elements + [new_element]
    return obj.Array(new_elements)


def builtin_puts(args):
    for arg in args:
        if arg is not None:
            print_line(arg.inspect())
    return NULL
