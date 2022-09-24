import src.kimchi_object as obj


def builtin_len(*args):
    if len(args) != 1:
        return obj.Error("wrong number of arguments. got={}, want=1".format(len(args)))
    arg = args[0]
    if isinstance(arg, obj.String):
        return obj.Integer(len(arg.value))
    else:
        return obj.Error("argument to `len` not supported, got {}".format(arg.type()))


builtins = {
    "len": obj.Builtin(builtin_len)
}
