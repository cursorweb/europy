import eotypes
from error.error import EoSyntaxError
import parser.nodes.exprn as Expr
from tokens import TType, Token


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.i = 0
    
    def run(self) -> Expr:
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
        if self.match(TType.Not, TType.Minus):
            op = self.prev()
            right = self.unary()
            return Expr.Unary(op, right)
        
        return self.primary()
    
    def primary(self):
        if self.match(TType.T_True): return Expr.Literal(eotypes.Bool(True))
        if self.match(TType.T_False): return Expr.Literal(eotypes.Bool(False))
        if self.match(TType.Nil): return Expr.Literal(eotypes.Nil())

        if self.match(TType.Number, TType.String):
            t = self.prev()
            if t.ttype == TType.String:
                return Expr.Literal(eotypes.String(t.data))
            else:
                return Expr.Literal(eotypes.Num(t.data))
        
        if self.match(TType.LeftParen):
            expr = self.expr()
            self.consume(TType.RightParen, "Expected ')' after grouping")
            return Expr.Grouping(expr)

        tok = self.peek()
        raise EoSyntaxError(tok, f"Unexpected token '{tok.ttype}'")


    """ Utils """
    def match(self, *types: list[TType]):
        for type in types:
            if self.check(type):
                self.next()
                return True
            
        return False
    
    def check(self, type: TType):
        if (self.is_end()): return False
        return self.peek().ttype == type
    
    def consume(self, token: TType, msg: str):
        if self.check(token):
            return self.next()
        
        # no sync-ing can be done
        # a raise terminates the whole process straight to catch
        raise EoSyntaxError(self.peek(), msg)
    

    """ Pos """
    def is_end(self):
        return self.peek().ttype == TType.EOF

    def peek(self, n = 0):
        return self.tokens[self.i + n]
    
    def prev(self):
        return self.tokens[self.i - 1]
    
    def next(self):
        if not self.is_end():
            self.i += 1
        return self.prev()