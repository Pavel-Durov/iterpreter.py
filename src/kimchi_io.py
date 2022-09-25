import os


def print_line(s):
    os.write(1, bytes(s))
    os.write(1, "\n")
