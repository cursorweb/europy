from abc import ABC, abstractmethod
from typing import Literal
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


class WhileStmt(Stmt):
    def __init__(self, cond: Expr, loop: list[Stmt]):
        self.cond = cond
        self.loop = loop
    
    def visit(self, v: StmtVisitor):
        return v.while_stmt(self)



class LoopFlow(Stmt):
    def __init__(self, type: Literal['break', 'continue']):
        self.type = type
    
    def visit(self, v: StmtVisitor):
        return v.loop_flow(self)



class RetStmt(Stmt):
    def __init__(self, val: Expr = None):
        self.val = val
    
    def visit(self, v: StmtVisitor):
        return v.ret_stmt(self)



class Function(Stmt):
    def __init__(self, name: Token, args: list[Token], opt_args: list[(Token, Expr)], block: list[Stmt]):
        self.name = name
        self.args = args
        self.opt_args = opt_args
        self.block = block
    
    def visit(self, v: StmtVisitor):
        return v.function(self)



# todo heeheh!
'''
class UseStmt(Stmt):
    def __init__(self, name: Token, ):
        self.
    
    def visit(self, v: StmtVisitor):
        return v.(self)
'''