from src.kimchi_evaluator import eval
from src.kimchi_io import print_line
from src.kimchi_lexer import Lexer
from src.kimchi_object import Environment
from src.kimchi_parser import Parser


def main():
    env = Environment()

    while True:
        s = raw_input("> ")

        if s == "":
            break
        lex = Lexer(s)
        p = Parser(lex)
        prog = p.parse_program()

        if len(p.errors) != 0:
            print_parse_errors(p.errors)
            continue

        evaluated = eval(prog, env)
        if evaluated != None:
            print_line(evaluated.inspect())


def print_parse_errors(errors):
    print_line("Woops! We ran into some errors here! Parser errors:")
    for error in errors:
        print_line(str(error))


if __name__ == "__main__":
    main()
