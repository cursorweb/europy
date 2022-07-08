from error.lf import LineInfo
from error import SyntaxError
from tokens import Token, TType


# todos: those cool errors (tm)
class Lexer:
    i = 0
    tokens: list[Token] = []

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
            elif char == '}':
                if self.match('}'): self.append_token(TType.RightBBrace)
                else: self.append_token(TType.RightBrace)
            elif char == '(':
                self.append_token(TType.LeftParen)
            elif char == ')':
                self.append_token(TType.RightParen)
            elif char == '[':
                self.append_token(TType.LeftBrack)
            elif char == ']':
                self.append_token(TType.RightBrack)
            elif char == '!':
                if self.match('='): self.append_token(TType.NotEq)
                else: self.append_token(TType.Not)
            elif char == '=':
                if self.match('='): self.append_token(TType.EqEq)
                else: self.append_token(TType.Eq)
            elif char == '>':
                if self.match('='): self.append_token(TType.GreaterEq)
                else: self.append_token(TType.Greater)
            elif char == '<':
                if self.match('='): self.append_token(TType.LessEq)
                else: self.append_token(TType.Less)
            elif char == '"' or char == "'":
                # lf = self.lf
                str_type = char
                string = ''

                while self.is_valid() and self.peek() != str_type:
                    if self.peek() == '\n':
                        self.newline()
                    
                    if self.peek() == '\\':
                        self.next()
                        c = self.peek()
                        self.next()

                        if c == 'n': string += '\n'
                        elif c == 'r': string += '\r'
                        elif c == 't': string += '\t'
                        elif c == 'a': string += '\x07'
                        elif c == 'b': string += '\x08'
                        elif c == 'e': string += '\x1b'
                        elif c == 'f': string += '\x0c'
                        elif c == 'v': string += '\x0b'
                        elif c == '\\': string += '\\'
                        elif c == "'": string += "'"
                        elif c == '"': string += '"'
                        elif c == '?': string += '?' # ?????
                        elif c == 'o':
                            esc = self.read_n(3)
                            try:
                                n = int(esc, 8)
                                string += chr(n)
                            except:
                                raise SyntaxError(f"Invalid string escape '\\o{esc}'")
                        elif c == 'x':
                            esc = self.read_n(2)
                            try:
                                n = int(esc, 16)
                                string += chr(n)
                            except:
                                raise SyntaxError(f"Invalid string escape '\\x{esc}'")
                        elif c == 'u':
                            esc = self.read_n(4)
                            try:
                                n = int(esc, 16)
                                string += chr(n)
                            except:
                                raise SyntaxError(f"Invalid string escape '\\u{esc}'")
                        elif c == 'U':
                            esc = self.read_n(8)
                            try:
                                n = int(esc, 16)
                                string += chr(n)
                            except:
                                raise SyntaxError(f"Invalid string escape '\\U{esc}'")
                        else:
                            string += self.peek()
                            self.next()

                if not self.is_valid():
                    raise SyntaxError(self.lf, "Unterminated string")
                
                self.next() # "
                self.append_token(TType.String, string)
            elif char == ',':
                self.append_token(TType.Comma)
            elif char == '.':
                if self.match('.'): self.append_token(TType.DotDot)
                elif self.match('='): self.append_token(TType.DotEq)
                else: self.append_token(TType.Dot)
            elif char == ';':
                self.append_token(TType.Semi)
            elif char == '?':
                self.append_token(TType.Question)
            elif char == ':':
                self.append_token(TType.Colon)
            elif char == '+':
                if self.match('='): self.append_token(TType.PlusEq)
                else: self.append_token(TType.Plus)
            elif char == '-':
                if self.match('='): self.append_token(TType.MinusEq)
                else: self.append_token(TType.Minus)
            elif char == '*':
                if self.match('='): self.append_token(TType.TimesEq)
                elif self.match('*'):
                    if self.match('='): self.append_token(TType.PowEq)
                    else: self.append_token(TType.Pow)
                else: self.append_token(TType.Times)
            elif char == '/':
                if self.match('='): self.append_token(TType.DivideEq)
                elif self.match('/'):
                    while self.peek() != '\n' and self.is_valid():
                        self.next()
                elif self.match('*'):
                    while self.is_valid() and (self.peek() != '*' and self.peek(1) != '/'):
                        if self.peek() == '\n': self.newline()
                        self.next()
                    
                    if not self.is_valid():
                        raise SyntaxError("Unterminated multiline comment")
                    
                    self.next() # *
                    self.next() # /
                else:
                    self.append_token(TType.Divide)
            elif char == ' ' or char == '\r' or char == '\t':
                pass
            elif char == '\n':
                self.newline()
            else:
                raise SyntaxError(self.lf, f"Unexpected token '{char}'")

            self.next()
        
        self.append_token(TType.EOF)
        return self.tokens
    

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
    
    def read_n(self, n):
        string = ''
        for _ in range(0, n):
            string += self.peek()
            self.next()
    
    def append_token(self, tok: TType, data = None):
        self.tokens.append(Token(tok, self.lf.copy(), data))


    def match(self, c: str):
        if self.peek() == c:
            self.next()
            return True
        return False