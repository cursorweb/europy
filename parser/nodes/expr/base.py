from abc import ABC, abstractmethod
from typing import Generic, TypeVar, TYPE_CHECKING

if TYPE_CHECKING:
    from parser.nodes.expr.node import *
    from parser.nodes.stmt.node import *

T = TypeVar("T")


# things like interpreter, resolver will 'implement' this
class ExprVisitor(ABC, Generic[T]):
    @abstractmethod
    def block_expr(self, e: "BlockExpr") -> T:
        raise Exception()

    @abstractmethod
    def if_expr(self, e: "IfExpr") -> T:
        raise Exception()

    @abstractmethod
    def while_expr(self, e: "WhileExpr") -> T:
        raise Exception()

    @abstractmethod
    def for_expr(self, e: "ForExpr") -> T:
        raise Exception()

    @abstractmethod
    # break and continue
    def loop_flow(self, e: "LoopFlow") -> T:
        raise Exception()

    @abstractmethod
    def return_expr(self, e: "ReturnExpr") -> T:
        raise Exception()

    @abstractmethod
    def assign(self, e: "Assign") -> T:
        raise Exception()

    @abstractmethod
    def binary(self, e: "Binary") -> T:
        raise Exception()

    @abstractmethod
    def grouping(self, e: "Grouping") -> T:
        raise Exception()

    @abstractmethod
    def literal(self, e: "LiteralVal") -> T:
        raise Exception()

    @abstractmethod
    def unary(self, e: "Unary") -> T:
        raise Exception()

    @abstractmethod
    def variable(self, e: "Variable") -> T:
        raise Exception()

    @abstractmethod
    def logical(self, e: "Logical") -> T:
        raise Exception()

    @abstractmethod
    def call(self, e: "Call") -> T:
        raise Exception()

    @abstractmethod
    def get(self, e: "Get") -> T:
        raise Exception()

    @abstractmethod
    def set(self, e: "Set") -> T:
        raise Exception()

    @abstractmethod
    def prop(self, e: "Prop") -> T:
        raise Exception()

    @abstractmethod
    def array(self, e: "ArrayExpr") -> T:
        raise Exception()

    @abstractmethod
    def map(self, e: "Map") -> T:
        raise Exception()

    @abstractmethod
    def range(self, e: "Range") -> T:
        raise Exception()


class Expr(ABC):
    @abstractmethod
    def visit(self, v: ExprVisitor[T]) -> T:
        raise Exception()
