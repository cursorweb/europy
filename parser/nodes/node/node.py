from abc import ABC, abstractmethod
from ..expr.base import Expr
from .base import StmtVisitor

from tokens import Token




class Stmt(ABC):
    @abstractmethod
    def visit(self, v: StmtVisitor): pass

class ExprStmt(Stmt):
    def __init__(self, expr: Expr) -> None:
        self.expr = expr