import src.kimchi_object.object as obj
from src.kimchi_ast.ast import BlockStatement, ExpressionStatement, IfExpression, InfixExpression, IntegerLiteral, \
    PrefixExpression, Program, Boolean, ReturnStatement

TRUE = obj.Boolean(True)
FALSE = obj.Boolean(False)
NULL = obj.Null()


def eval(node):
    # statements
    if isinstance(node, Program):
        return eval_program(node)
    elif isinstance(node, ExpressionStatement):
        return eval(node.expression)
    elif isinstance(node, ReturnStatement):
        val = eval(node.return_value)
        if isinstance(val, obj.Error):
            return val
        return obj.ReturnValue(val)
    elif isinstance(node, BlockStatement):
        return eval_block_statement(node)

    # expressions
    if isinstance(node, IntegerLiteral):
        return obj.Integer(node.value)
    elif isinstance(node, Boolean):
        return native_bool_to_boolean_object(node.value)
    elif isinstance(node, PrefixExpression):
        right = eval(node.right)
        if isinstance(right, obj.Error):
            return right
        return eval_prefix_expression(node.operator, right)
    elif isinstance(node, InfixExpression):
        left = eval(node.left)
        if isinstance(left, obj.Error):
            return left
        right = eval(node.right)
        if isinstance(right, obj.Error):
            return right
        return eval_infix_expression(node.operator, left, right)
    
    elif isinstance(node, IfExpression):
        return eval_if_expression(node)

    return None


def eval_block_statement(block):
    result = None
    for statement in block.statements:
        result = eval(statement)
        if result is not None:
            if isinstance(result, obj.ReturnValue) or isinstance(result, obj.Error):
                return result
    return result


def eval_program(prog):
    result = None

    for statement in prog.statements:
        result = eval(statement)
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


def eval_if_expression(node):
    condition = eval(node.condition)
    if isinstance(condition, obj.Error):
        return condition
    if is_truthy(condition):
        return eval(node.consequence)
    elif node.alternative is not None:
        return eval(node.alternative)
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
