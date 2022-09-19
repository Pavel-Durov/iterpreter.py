from src.lexer import Lexer
from src.tk import Tk


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


if __name__ == "__main__":
    main()
