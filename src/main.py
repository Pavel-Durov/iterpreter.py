from src.kimchi_evaluator.evaluator import Evaluator
from src.kimchi_io import print_line
from src.kimchi_ioc import IOC
from src.kimchi_lexer import Lexer
from src.kimchi_parser.parser import Parser


def run(program_contents, ioc):
    lexer = Lexer(program_contents)
    parser = Parser(lexer)
    program = parser.parse_program()
    e = Evaluator(ioc)
    e.eval(program, ioc.create_env())


def entry_point(argv):
    try:
        fp = argv[1]
    except IndexError:
        print_line("You must supply a filename")
        return 1

    ioc = IOC()
    if len(argv) > 2:
        self_like_opt = argv[2]
        ioc.set_self_like(self_like_opt == 'self-like')

    with open(fp, "r") as f:
        program_contents = f.read()

    ioc.print_config()
    run(program_contents, ioc)
    return 0


def target(*args):
    return entry_point, None


if __name__ == "__main__":
    import sys

    entry_point(sys.argv)
