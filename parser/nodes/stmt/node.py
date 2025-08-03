from typing import Literal
from enum import Enum
from ..expr.base import Expr
from .base import Stmt, StmtVisitor

from tokens import Token


"""
class (Stmt):
    def __init__(self, ):
        self.
    
    def visit(self, v: StmtVisitor):
        return v.(self)
"""


class ExprStmt(Stmt):
    def __init__(self, expr: Expr):
        self.expr = expr

    def visit(self, v: StmtVisitor):
        return v.expr_stmt(self)


class VarDecl(Stmt):
    def __init__(self, decls: list[tuple[str, Expr]]):
        self.decls = decls

    def visit(self, v: StmtVisitor):
        return v.var_decl(self)


class BlockStmt(Stmt):
    def __init__(self, stmts: list[Stmt]):
        self.stmts = stmts

    def visit(self, v: StmtVisitor):
        return v.block_stmt(self)


class IfStmt(Stmt):
    def __init__(
        self,
        cond: Expr,
        if_true: list[Stmt],
        elifs: list[tuple[Expr, list[Stmt]]],
        els: list[Stmt] | None = None,
    ):
        self.cond = cond
        self.if_true = if_true
        self.elifs = elifs
        self.els = els

    def visit(self, v: StmtVisitor):
        return v.if_stmt(self)


class WhileStmt(Stmt):
    def __init__(self, cond: Expr, loop: list[Stmt]):
        self.cond = cond
        self.block = loop

    def visit(self, v: StmtVisitor):
        return v.while_stmt(self)


class ForStmt(Stmt):
    def __init__(self, name: str, iterator: Expr, block: list[Stmt]) -> None:
        self.name = name
        self.iter = iterator
        self.block = block

    def visit(self, v: StmtVisitor):
        return v.for_stmt(self)


class LoopFlow(Stmt):
    def __init__(self, token: Token, type: Literal["break", "continue"]):
        self.token = token
        self.type = type

    def visit(self, v: StmtVisitor):
        return v.loop_flow(self)


class RetStmt(Stmt):
    def __init__(self, ret: Token, val: Expr | None = None):
        self.token = ret
        self.val = val

    def visit(self, v: StmtVisitor):
        return v.ret_stmt(self)


class ParamType(Enum):
    Named = "named"
    Optional = "optional"


class Function(Stmt):
    def __init__(
        self,
        name: Token,
        args: list[Token],
        opt_args: list[tuple[Token, Expr]],
        block: list[Stmt],
    ):
        """
        strategy: fill up as many args as possible,
        then fill up opt_args.
        Finally, used named variables to assign guys by creating a map str -> index
        """
        self.name = name
        self.params = args
        self.opt_params = opt_args
        self.block = block

    def visit(self, v: StmtVisitor):
        return v.function(self)


class UseStmt(Stmt):
    class ImportType:
        mods: list[Token]

        def __init__(self):
            # empty = use io;
            # mult = use io.{println, print, readln};
            self.mods = []
            # all = use io.*;
            self.all = False

        @classmethod
        def mod(cls):
            """`use io;`"""
            return cls()

        @classmethod
        def star(cls):
            """`use io.*;`"""
            out = cls()
            out.all = True
            return out

        @classmethod
        def mult(cls, names: list[Token]):
            """`use io.{println, print};`"""
            out = cls()
            out.mods = names
            return out

    def __init__(self, name: Token, imp_type: ImportType):
        self.name = name
        self.imp_type = imp_type

    def visit(self, v: StmtVisitor):
        return v.use_stmt(self)
