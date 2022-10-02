from rpython.jit.codewriter.policy import JitPolicy
from rpython.rlib.jit import JitDriver, elidable, hint

import src.kimchi_ast as ast
import src.kimchi_object as obj
from src.kimchi_ast.ast import InfixExpression
from src.kimchi_evaluator.const import TRUE, FALSE, NULL
from src.kimchi_io import print_line


def jitpolicy(driver):
    return JitPolicy()


def get_location(node, self):
    return "[KIMCHI] evaluating %s " % (str(node))


jitdriver = JitDriver(greens=["node", "self"], reds=["env"], get_printable_location=get_location)


class Evaluator():
    builtins = {
        "len": True,
        "first": True,
        "last": True,
        "rest": True,
        "push": True,
        "puts": True,
    }

    def __init__(self, ioc):
        self.ioc = hint(ioc)
        self.builtins = hint(self.builtins)

    def create_env(self, env):
        return self.ioc.create_env(env)

    def eval_program(self, statements, env):
        result = None
        pc = 0
        while pc < len(statements):
            stmt = statements[pc]
            # In loop merge point doesnt produce logs probably cause for the recursive nature of eval
            # jitdriver.jit_merge_point(pc=pc, stmt=stmt, statements=statements, result=result, env=env, self=self)
            result = self.eval(stmt, env)
            if isinstance(result, obj.ReturnValue):
                return result.value
            elif isinstance(result, obj.Error):
                return result
            pc += 1

        return result

    def eval(self, node, env):
        jitdriver.jit_merge_point(node=node, env=env, self=self)
        if isinstance(node, ast.Program):
            return self.eval_program(node.statements, env)
        elif isinstance(node, ast.HashLiteral):
            return self.eval_hash_literal(node, env)
        elif isinstance(node, ast.IndexExpression):
            left = self.eval(node.left, env)
            if isinstance(left, obj.Error):
                return left
            index = self.eval(node.index, env)
            if isinstance(index, obj.Error):
                return index
            return self.eval_index_expression(left, index)
        elif isinstance(node, ast.StringLiteral):
            return obj.String(node.value)
        elif isinstance(node, ast.ArrayLiteral):
            elements = self.eval_expressions(node.elements, env)
            if len(elements) == 1 and isinstance(elements[0], obj.Error):
                return elements[0]
            return obj.Array(elements)
        elif isinstance(node, ast.ExpressionStatement):
            return self.eval(node.expression, env)
        elif isinstance(node, ast.ReturnStatement):
            val = self.eval(node.return_value, env)
            if isinstance(val, obj.Error):
                return val
            return obj.ReturnValue(val)
        elif isinstance(node, ast.BlockStatement):
            return self.eval_block_statement(node, env)
        elif isinstance(node, ast.CallExpression):
            func = self.eval(node.function, env)
            if isinstance(func, obj.Error):
                return func
            args = self.eval_expressions(node.arguments, env)
            if len(args) == 1 and isinstance(args[0], obj.Error):
                return args[0]
            return self.apply_function(func, args)
        elif isinstance(node, ast.FunctionLiteral):
            return obj.Function(node.parameters, node.body, env)
        elif isinstance(node, ast.IntegerLiteral):
            return obj.Integer(node.value)
        elif isinstance(node, ast.LetStatement):
            val = self.eval(node.value, env)
            if isinstance(val, obj.Error):
                return val
            env.set(node.name.value, val)
        elif isinstance(node, ast.AssignStatement):
            val = self.eval(node.value, env)
            if isinstance(val, obj.Error):
                return val
            env.set(node.name.value, val)
        elif isinstance(node, ast.Identifier):
            return self.eval_identifier(node, env)
        elif isinstance(node, ast.Boolean):
            return self.native_bool_to_boolean_object(node.value)
        elif isinstance(node, ast.PrefixExpression):
            right = self.eval(node.right, env)
            if isinstance(right, obj.Error):
                return right
            return self.eval_prefix_expression(node.operator, right)
        elif isinstance(node, ast.InfixExpression):
            return self.eval_infix_expression(node, env)
        elif isinstance(node, ast.IfExpression):
            return self.eval_if_expression(node, env)
        elif isinstance(node, ast.WhileExpression):
            return self.eval_while_expression(node, env)

        return None

    def eval_hash_literal(self, node, env):
        pairs = {}

        for key_node, value_node in node.pairs.items():
            key = self.eval(key_node, env)
            if isinstance(key, obj.Error):
                return key
            value = self.eval(value_node, env)
            if isinstance(value, obj.Error):
                return value
            if isinstance(value, obj.HashableObject):
                hashed = key.hash_key()
                pairs[hashed] = obj.HashPair(key, value)

        return obj.Hash(pairs)

    def eval_hash_index_expression(self, hash, index):
        if not isinstance(index, obj.HashableObject):
            return obj.Error("unusable as hash key: %s" % (index.type()))
        pair = hash.pairs.get(index.hash_key())
        if pair:
            return pair.value
        return NULL

    def eval_index_expression(self, left, index):
        if isinstance(left, obj.Array) and isinstance(index, obj.Integer):
            return self.eval_array_index_expression(left, index)
        elif isinstance(left, obj.Hash):
            return self.eval_hash_index_expression(left, index)
        return obj.Error("index operator not supported: %s" % (left.type()))

    def eval_array_index_expression(self, array, index):
        idx = index.value
        max = len(array.elements) - 1
        if idx < 0 or idx > max:
            return NULL
        return array.elements[idx]

    def unwrap_return_value(self, wrapper):
        if isinstance(wrapper, obj.ReturnValue):
            return wrapper.value
        return wrapper

    def extend_function_env(self, fn, args):
        env = self.create_env(fn.env)

        for param_idx, param in enumerate(fn.parameters):
            env.set(param.value, args[param_idx])

        return env

    def apply_function(self, fn, args):
        if isinstance(fn, obj.Function):
            extended_env = self.extend_function_env(fn, args)
            evaluated = self.eval(fn.body, extended_env)
            return self.unwrap_return_value(evaluated)
        if args is None:
            return None
        if fn.name == "len":
            if isinstance(args, list) and len(args) == 1:
                return self.builtin_len(args[0])
            else:
                return obj.Error("wrong number of arguments. got=%d, want=1" % (len(args)))
        elif fn.name == "puts":
            return self.builtin_puts(args)
        elif fn.name == "first":
            return self.builtin_first(args)
        elif fn.name == "last":
            return self.builtin_last(args)
        elif fn.name == "rest":
            return self.builtin_rest(args)
        elif fn.name == "push":
            return self.builtin_push(args)
        return obj.Error("not a function: %s" % (fn.type()))

    def eval_expressions(self, args, env):
        result = []
        for arg in args:
            evaluated = self.eval(arg, env)
            if isinstance(evaluated, obj.Error):
                return [evaluated]
            result.append(evaluated)
        return result

    def eval_identifier(self, node, env):
        val = env.get(node.value)
        if val:
            return val
        if node.value in self.builtins:
            return obj.Builtin(node.value)
        return obj.Error("identifier not found: %s" % (node.value))

    def eval_block_statement(self, block, env):
        result = None
        for statement in block.statements:
            result = self.eval(statement, env)
            if result is not None:
                if isinstance(result, obj.ReturnValue) or isinstance(result, obj.Error):
                    return result
        return result

    def is_truthy(self, obj):
        if obj == NULL:
            return False
        if obj == TRUE:
            return True
        if obj == FALSE:
            return False
        return True

    def eval_while_expression(self, node, env):
        result = NULL
        while True:
            condition = self.eval(node.condition, env)
            if isinstance(condition, obj.Error):
                return condition
            if not self.is_truthy(condition):
                return result
            result = self.eval(node.body, env)

    def eval_if_expression(self, node, env):
        condition = self.eval(node.condition, env)
        if isinstance(condition, obj.Error):
            return condition
        if self.is_truthy(condition):
            return self.eval(node.consequence, env)
        elif node.alternative is not None:
            return self.eval(node.alternative, env)
        return NULL

    @elidable
    def is_plus(self, node):
        return node.operator == ast.InfixExpression.PLUS

    @elidable
    def is_minus(self, node):
        return node.operator == ast.InfixExpression.MINUS

    @elidable
    def is_mul(self, node):
        return node.operator == ast.InfixExpression.MUL

    @elidable
    def is_divide(self, node):
        return node.operator == ast.InfixExpression.DIV

    @elidable
    def is_less_than(self, node):
        return node.operator == ast.InfixExpression.LT

    @elidable
    def is_greater_than(self, node):
        return node.operator == ast.InfixExpression.GT

    @elidable
    def is_greater_than(self, node):
        return node.operator == ast.InfixExpression.GT

    @elidable
    def is_greater_eq(self, node):
        return node.operator == ast.InfixExpression.EQ

    @elidable
    def is_greater_not_eq(self, node):
        return node.operator == ast.InfixExpression.NOT_EQ

    def eval_integer_infix_expression(self, node, left, right):
        left_val = left.value
        right_val = right.value
        if self.is_plus(node):
            return obj.Integer(left_val + right_val)
        elif self.is_minus(node):
            return obj.Integer(left_val - right_val)
        elif self.is_mul(node):
            return obj.Integer(left_val * right_val)
        elif self.is_divide(node):
            return obj.Integer(left_val / right_val)
        elif self.is_less_than(node):
            return self.native_bool_to_boolean_object(left_val < right_val)
        elif self.is_greater_than(node):
            return self.native_bool_to_boolean_object(left_val > right_val)
        elif self.is_greater_eq(node):
            return self.native_bool_to_boolean_object(left_val == right_val)
        elif self.is_greater_not_eq(node):
            return self.native_bool_to_boolean_object(left_val != right_val)
        return obj.Error(
            "unknown operator: %s %s %s" % (str(left.type()), str(node.literal_operator), str(right.type())))

    def eval_infix_expression(self, node, env):
        left = self.eval(node.left, env)
        if isinstance(left, obj.Error):
          return left
        
        right = self.eval(node.right, env)
        if isinstance(right, obj.Error):
          return right      

        if isinstance(left, obj.Integer) and isinstance(right, obj.Integer):
            return self.eval_integer_infix_expression(node, left, right)
        elif node.operator == InfixExpression.EQ:
            return self.native_bool_to_boolean_object(left == right)
        elif node.operator == InfixExpression.NOT_EQ:
            return self.native_bool_to_boolean_object(left != right)
        elif isinstance(left, obj.String) and isinstance(right, obj.String):
            return self.eval_string_infix_expression(left, right, node)
        elif left.type() != right.type():
            return obj.Error("type mismatch: %s %s %s" % (left.type(), node.literal_operator, right.type()))
        return obj.Error("unknown operator: %s %s %s" % (left.type(), node.literal_operator, right.type()))

    def eval_string_infix_expression(self, left, right, node):
        if node.operator != InfixExpression.PLUS:
            return obj.Error("Unknown operator: %s %s %s" % (left.type(), node.literal_operator, right.type()))
        return obj.String(left.value + right.value)

    def eval_bang_operator_expression(self, right):
        if right == TRUE:
            return FALSE
        if right == FALSE:
            return TRUE
        if right == NULL:
            return TRUE
        return FALSE

    def eval_minus_prefix_operator_expression(self, right):
        if isinstance(right, obj.Integer):
            return obj.Integer(-right.value)

        return obj.Error("unknown operator: -%s" % (right.type()))

    def eval_prefix_expression(self, operator, right):
        if operator == "!":
            return self.eval_bang_operator_expression(right)
        elif operator == "-":
            return self.eval_minus_prefix_operator_expression(right)
        return obj.Error("unknown operator: %s" % (operator, right.type()))

    def native_bool_to_boolean_object(self, input):
        if input:
            return TRUE
        return FALSE

    def builtin_len(self, arg):
        if isinstance(arg, obj.String):
            return obj.Integer(len(arg.value))
        elif isinstance(arg, obj.Array):
            return obj.Integer(len(arg.elements))
        else:
            return obj.Error("argument to `len` not supported, got %s" % (arg.type()))

    def builtin_first(self, args):
        if len(args) != 1:
            return obj.Error("wrong number of arguments. got=%d, want=1" % (len(args)))
        arg = args[0]
        if not isinstance(arg, obj.Array):
            return obj.Error("argument to `first` must be ARRAY, got %s" % (arg.type()))
        if len(arg.elements) > 0:
            return arg.elements[0]
        else:
            return NULL

    def builtin_last(self, args):
        if len(args) != 1:
            return obj.Error("wrong number of arguments. got=%d, want=1" % (len(args)))
        arg = args[0]
        if not isinstance(arg, obj.Array):
            return obj.Error("argument to `last` must be ARRAY, got %s" % (arg.type()))
        if len(arg.elements) > 0:
            return arg.elements[-1]
        else:
            return NULL

    def builtin_rest(self, args):
        if len(args) != 1:
            return obj.Error("wrong number of arguments. got=%d, want=1" % (len(args)))
        arg = args[0]
        if not isinstance(arg, obj.Array):
            return obj.Error("argument to `rest` must be ARRAY, got %s" % (arg.type()))
        if len(arg.elements) > 0:
            return obj.Array(arg.elements[1:])
        else:
            return NULL

    def builtin_push(self, args):
        if len(args) != 2:
            return obj.Error("wrong number of arguments. got=%d, want=2" % len(args))
        arg = args[0]
        if not isinstance(arg, obj.Array):
            return obj.Error("argument to `push` must be ARRAY, got %s" % (arg.type()))
        new_element = args[1]
        new_elements = arg.elements + [new_element]
        return obj.Array(new_elements)

    def builtin_puts(self, args):
        for arg in args:
            if arg is not None:
                print_line(arg.inspect())
        return NULL
