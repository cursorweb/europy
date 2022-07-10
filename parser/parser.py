import parser.nodes.exprn as Expr
from tokens import TType, Token


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.i = 0
    
    def run(self):
        return self.expr()
    

    """ AST """
    def expr(self):
        return self.equality()
    
    def equality(self):
        expr = self.comp()

        while self.match(TType.NotEq, TType.EqEq):
            op = self.prev()
            right = self.comp()
            expr = Expr.Binary(expr, op, right)
        
        return expr
    
    def comp(self):
        expr = self.add()

        while self.match(TType.Less, TType.LessEq, TType.Greater, TType.GreaterEq):
            op = self.prev()
            right = self.add()
            expr = Expr.Binary(expr, op, right)
        
        return expr
    
    def add(self):
        expr = self.mult()

        while self.match(TType.Plus, TType.Minus):
            op = self.prev()
            right = self.mult()
            expr = Expr.Binary(expr, op, right)
        
        return expr
    
    def mult(self):
        expr = self.unary()

        while self.match(TType.Times, TType.Divide, TType.Mod):
            op = self.prev()
            right = self.unary()
            expr = Expr.Binary(expr, op, right)
        
        return expr
    
    def unary(self):
        


    """ Utils """
    def match(self, *types: list[TType]):
        for type in types:
            if self.check(type):
                self.advance()
                return True
            
        return False
    
    def check(self, type: TType):
        if (self.is_end()): return False
        return self.peek().ttype == type
    
    def is_end(self):
        return self.peek().ttype == TType.EOF

    def peek(self, n = 0):
        return self.tokens[self.i + n]
    
    def prev(self):
        return self.tokens[self.i - 1]