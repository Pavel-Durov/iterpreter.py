from src.kimchi_lexer import Lexer
from src.kimchi_parser.parser import Parser
from src.kimchi_evaluator import eval
from src.kimchi_object import Environment


def run(program_contents):
    lexer = Lexer(program_contents)
    parser = Parser(lexer)
    program = parser.parse_program()
    eval(program, Environment())


def entry_point(argv):
    try:
        fp = argv[1]
    except IndexError:
        print("You must supply a filename")
        return 1

    with open(fp, "r") as f:
        program_contents = f.read()

    run(program_contents)
    return 0

def target(*args):
    return entry_point, None


if __name__ == "__main__":
    import sys
    entry_point(sys.argv)
