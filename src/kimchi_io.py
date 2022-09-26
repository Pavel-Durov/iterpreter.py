import os


def print_line(s):
    os.write(1, bytes(s))
    os.write(1, bytes("\n"))
    # os.write(1, bytes(s, "utf-8"))
    # os.write(1, bytes("\n", "utf-8"))
