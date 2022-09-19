from src.kimchi_lexer import Lexer


def entry_point(argv):
    print("Hello, world!")
    Lexer("2+2=3")
    return 0


def target(*args):
    return entry_point, None


if __name__ == "__main__":
    import sys

    entry_point(sys.argv)
