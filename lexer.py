from error.lf import LineInfo
from error import SyntaxError
from tokens import Token, TType


class Lexer:
    i = 0
    tokens = []

    code: str
    lenc: int
    """ LEN(Code) """
    lf: LineInfo


    def __init__(self) -> None:
        self.i = 0
        self.tokens = []
    
    @classmethod
    def from_file(cls, file: str) -> 'Lexer':
        lexer = cls()

        f = open(file, 'r')
        code = f.read()
        f.close()

        lexer.code = code
        lexer.lenc = len(code)

        lexer.lf = LineInfo(file, 1, 1)
        
        return lexer

    @classmethod
    def from_repl(cls, code: str) -> 'Lexer':
        lexer = cls()

        lexer.code = code
        lexer.lenc = len(code)

        lexer.lf = LineInfo("<repl>", 1, 1)

        return lexer
    

    def run(self):
        while self.is_valid():
            char = self.code[self.i]

            if char == '{':
                if self.match('{'): self.append_token(TType.LeftBBrace)
                else: self.append_token(TType.LeftBrace)
            else:
                raise SyntaxError(self.lf, f"Unexpected token '{char}'")

            self.next()
    

    """ Helpers """
    def is_valid(self):
        return self.i < self.lenc
    
    def next(self):
        self.i += 1
        self.lf.col += 1
    
    def newline(self):
        """ newline resets the col, but self.next() will still be called """
        self.lf.col = 0
        self.lf.line += 1
    
    def peek(self, n = 1):
        if not self.is_valid(): return '\0'
        return self.code[self.i + n]
    
    def append_token(self, ttype: TType, data = None):
        self.tokens.append(Token(ttype, self.lf, data))


    def match(self, c: str):
        if self.peek() == c:
            self.next()
            return True
        return False