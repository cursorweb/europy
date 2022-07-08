from error.lf import LineInfo
from tokens import Token, TType

class Lexer:
    i = 0
    tokens = []

    code: str
    lenc: int
    """ LEN(Code) """

    def __init__(self, file: str) -> None:
        f = open(file, 'r')
        code = f.read()
        f.close()

        self.code = code
        self.lenc = len(code)

        self.lf = LineInfo(file, 1, 1)

    def from_repl(self, code: str) -> None:
        self.code = code
        self.lenc = len(code)

        self.lf = LineInfo("<repl>", 1, 1)
    
    def run(self):
        while self.is_valid():
            char = self.code[self.i]

            if char == '{':
                if self.match('{'): self.append_token(TType.LeftBBrace)
                else: self.append_token(TType.LeftBrace)

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