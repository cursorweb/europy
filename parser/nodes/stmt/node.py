from enum import Enum
from ..expr.base import Expr
from .base import Stmt, StmtVisitor

from tokens import Token

# todo: remove statements
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


class ParamType(Enum):
    Named = "named"
    Optional = "optional"


class FunctionDecl(Stmt):
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
        return v.fn_decl(self)


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
