import eotypes
from error.error import EoSyntaxError

from parser.nodes.expr.base import Expr as ExprT
import parser.nodes.expr.node as Expr

from parser.nodes.stmt.base import Stmt as StmtT
import parser.nodes.stmt.node as Stmt

from tokens import TType, Token


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.i = 0
    
    def run(self) -> Expr:
        stmts = []

        while not self.is_end():
            stmts.append(self.stmt())
        
        return stmts
    

    """ - AST - """
    """ Stmt """
    def stmt(self) -> StmtT:
        return self.expr_stmt()
    
    def expr_stmt(self) -> StmtT:
        expr = self.expr()

        if not self.match(TType.Semi):
            semi = self.peek()
            if semi.ttype != TType.RightBrace: # semi.ttype != TType.eof ??
                raise EoSyntaxError(semi.lf, "Expected ';' after statement.")
        
        return expr


    """ Expr """
    def expr(self) -> ExprT:
        return self.equality()
    
    def equality(self) -> ExprT:
        expr = self.comp()

        while self.match(TType.NotEq, TType.EqEq):
            op = self.prev()
            right = self.comp()
            expr = Expr.Binary(expr, op, right)
        
        return expr
    
    def comp(self) -> ExprT:
        expr = self.add()

        while self.match(TType.Less, TType.LessEq, TType.Greater, TType.GreaterEq):
            op = self.prev()
            right = self.add()
            expr = Expr.Binary(expr, op, right)
        
        return expr
    
    def add(self) -> ExprT:
        expr = self.mult()

        while self.match(TType.Plus, TType.Minus):
            op = self.prev()
            right = self.mult()
            expr = Expr.Binary(expr, op, right)
        
        return expr
    
    def mult(self) -> ExprT:
        expr = self.unary()

        while self.match(TType.Times, TType.Divide, TType.Mod):
            op = self.prev()
            right = self.unary()
            expr = Expr.Binary(expr, op, right)
        
        return expr
    
    def unary(self) -> ExprT:
        if self.match(TType.Not, TType.Minus):
            op = self.prev()
            right = self.unary()
            return Expr.Unary(op, right)
        
        return self.primary()
    
    def primary(self) -> ExprT:
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
    def is_end(self) -> ExprT:
        return self.peek().ttype == TType.EOF

    def peek(self, n = 0):
        return self.tokens[self.i + n]
    
    def prev(self) -> ExprT:
        return self.tokens[self.i - 1]
    
    def next(self) -> ExprT:
        if not self.is_end():
            self.i += 1
        return self.prev()