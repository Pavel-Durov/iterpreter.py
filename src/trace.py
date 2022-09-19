trace_level = 0


def trace(msg):
    global trace_level
    trace_level += 1
    # print("." * trace_level + msg)


def untrace(msg):
    global trace_level
    # print("." * trace_level +msg)
    trace_level -= 1
