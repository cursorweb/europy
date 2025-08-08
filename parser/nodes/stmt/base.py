from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .node import *


# interpreter will extend both
class StmtVisitor(ABC):
    @abstractmethod
    def expr_stmt(self, e: "ExprStmt"):
        raise Exception()

    @abstractmethod
    def var_decl(self, e: "VarDecl"):
        raise Exception()

    @abstractmethod
    def fn_decl(self, e: "FunctionDecl"):
        raise Exception()

    @abstractmethod
    def use_stmt(self, e: "UseStmt"):
        raise Exception()


class Stmt(ABC):
    @abstractmethod
    def visit(self, v: StmtVisitor):
        raise Exception()
