from abc import ABC, abstractmethod
from ..expr.base import Expr
from .base import StmtVisitor

from tokens import Token


"""



class (Stmt):
    def __init__(self, ):
        self.
    
    def visit(self, v: StmtVisitor):
        return v.(self)
"""


class Stmt(ABC):
    @abstractmethod
    def visit(self, v: StmtVisitor): pass


class ExprStmt(Stmt):
    def __init__(self, expr: Expr):
        self.expr = expr

    def visit(self, v: StmtVisitor):
        return v.expr_stmt(self)


class VarDecl(Stmt):
    def __init__(self, decls: list[(str, Expr)]):
        self.decls = decls

    def visit(self, v: StmtVisitor):
        return v.var_decl(self)


class Block(Stmt):
    def __init__(self, stmts: list[Stmt]):
        self.stmts = stmts

    def visit(self, v: StmtVisitor):
        return v.block(self)


class IfStmt(Stmt):
    def __init__(self, cond: Expr, if_true: list[Stmt], elifs: list[(Expr, list[Stmt])], els: list[Stmt] = None):
        self.cond = cond
        self.if_true = if_true
        self.elifs = elifs
        self.els = els

    def visit(self, v: StmtVisitor):
        return v.if_stmt(self)
