import os
from src.awk_lexer import Lexer
from src.awk_tk import Tk


def main():
    while True:
        s = raw_input(">")

        if s == "":
            break
        lex = Lexer(s)
        tk = lex.next_token()

        while tk.type != Tk.EOF:
            print(tk)
            tk = lex.next_token()

def print_parse_errors(errors):
    for error in errors:
        os.write(1, str(error + "\n"))


if __name__ == "__main__":
    main()
