import os
from src.awk_lexer import Lexer
from src.awk_parser import Parser
from src.awk_tk import Tk


def main():
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

        os.write(1, str(prog))
        os.write(1, "\n")

def print_parse_errors(errors):
    os.write(1, str("Woops! We ran into some errors here! Parser errors: \n"))
    for error in errors:
        os.write(1, str(error + "\n"))


if __name__ == "__main__":
    main()
