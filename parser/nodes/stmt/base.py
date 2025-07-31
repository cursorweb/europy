from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .node import *


# interpreter will extend both
class StmtVisitor(ABC):
    @abstractmethod
    def expr_stmt(self, e: "ExprStmt"):
        pass

    @abstractmethod
    def var_decl(self, e: "VarDecl"):
        pass

    @abstractmethod
    def block_stmt(self, e: "BlockStmt"):
        pass

    @abstractmethod
    def if_stmt(self, e: "IfStmt"):
        pass

    @abstractmethod
    def while_stmt(self, e: "WhileStmt"):
        pass

    @abstractmethod
    # break and continue
    def loop_flow(self, e: "LoopFlow"):
        pass

    @abstractmethod
    def ret_stmt(self, e: "RetStmt"):
        pass

    @abstractmethod
    def function(self, e: "Function"):
        pass

    @abstractmethod
    def use_stmt(self, e: "UseStmt"):
        pass


class Stmt(ABC):
    @abstractmethod
    def visit(self, v: StmtVisitor):
        pass
