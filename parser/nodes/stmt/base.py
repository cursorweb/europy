from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Generic, TypeVar

if TYPE_CHECKING:
    from .node import *

T = TypeVar("T", default=None)


# interpreter will extend both
class StmtVisitor(ABC, Generic[T]):
    @abstractmethod
    def expr_stmt(self, e: "ExprStmt") -> T:
        raise Exception()

    @abstractmethod
    def var_decl(self, e: "VarDecl") -> T:
        raise Exception()

    @abstractmethod
    def fn_decl(self, e: "FunctionDecl") -> T:
        raise Exception()

    @abstractmethod
    def use_stmt(self, e: "UseStmt") -> T:
        raise Exception()


class Stmt(ABC):
    @abstractmethod
    def visit(self, v: StmtVisitor[T]) -> T:
        raise Exception()
