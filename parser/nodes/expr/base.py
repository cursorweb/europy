from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from parser.nodes.expr.node import *
    from parser.nodes.stmt.node import *

T = TypeVar("T")


# things like interpreter, resolver will 'implement' this
class ExprVisitor(ABC, Generic[T]):
    @abstractmethod
    def assign(self, e: "Assign") -> T:
        pass

    @abstractmethod
    def binary(self, e: "Binary") -> T:
        pass

    @abstractmethod
    def grouping(self, e: "Grouping") -> T:
        pass

    @abstractmethod
    def literal(self, e: "LiteralVal") -> T:
        pass

    @abstractmethod
    def unary(self, e: "Unary") -> T:
        pass

    @abstractmethod
    def variable(self, e: "Variable") -> T:
        pass

    @abstractmethod
    def block_expr(self, e: "BlockExpr") -> T:
        pass

    @abstractmethod
    def logical(self, e: "Logical") -> T:
        pass

    @abstractmethod
    def call(self, e: "Call") -> T:
        pass

    @abstractmethod
    def if_expr(self, e: "IfExpr") -> T:
        pass

    @abstractmethod
    def get(self, e: "Get") -> T:
        pass

    @abstractmethod
    def set(self, e: "Set") -> T:
        pass

    @abstractmethod
    def prop(self, e: "Prop") -> T:
        pass

    @abstractmethod
    def array(self, e: "Array") -> T:
        pass

    @abstractmethod
    def map(self, e: "Map") -> T:
        pass

    @abstractmethod
    def range(self, e: "Range") -> T:
        pass


class Expr(ABC):
    @abstractmethod
    def visit(self, v: ExprVisitor[T]) -> T:
        pass
