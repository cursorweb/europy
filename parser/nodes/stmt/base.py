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
    def block_stmt(self, e: "BlockStmt"):
        raise Exception()

    @abstractmethod
    def if_stmt(self, e: "IfStmt"):
        raise Exception()

    @abstractmethod
    def while_stmt(self, e: "WhileStmt"):
        raise Exception()

    @abstractmethod
    def for_stmt(self, e: "ForStmt"):
        raise Exception()

    @abstractmethod
    # break and continue
    def loop_flow(self, e: "LoopFlow"):
        raise Exception()

    @abstractmethod
    def return_stmt(self, e: "ReturnStmt"):
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
