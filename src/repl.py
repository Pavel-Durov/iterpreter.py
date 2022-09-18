from src.lexer import Lexer
from src.token import Token
from time import sleep

def main():
    while True:
        s = raw_input('>')
          
        if s == '':
            break
        lex = Lexer(s)
        tk = lex.next_token() 
        
        while tk.type != Token.EOF:
            print(tk)
            tk = lex.next_token()


if __name__ == '__main__':
    main()
  