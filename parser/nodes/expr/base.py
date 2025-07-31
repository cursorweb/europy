from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


# things like interpreter, resolver will 'implement' this
class ExprVisitor(ABC, Generic[T]):
    @abstractmethod
    def assign(self, e) -> T:
        pass

    @abstractmethod
    def binary(self, e) -> T:
        pass

    @abstractmethod
    def grouping(self, e) -> T:
        pass

    @abstractmethod
    def literal(self, e) -> T:
        pass

    @abstractmethod
    def unary(self, e) -> T:
        pass

    @abstractmethod
    def variable(self, e) -> T:
        pass

    @abstractmethod
    def block_expr(self, e) -> T:
        pass

    @abstractmethod
    def logical(self, e) -> T:
        pass

    @abstractmethod
    def ternary(self, e) -> T:
        pass

    @abstractmethod
    def call(self, e) -> T:
        pass

    @abstractmethod
    def if_expr(self, e) -> T:
        pass

    @abstractmethod
    def get(self, e) -> T:
        pass

    @abstractmethod
    def set(self, e) -> T:
        pass

    @abstractmethod
    def prop(self, e) -> T:
        pass

    @abstractmethod
    def array(self, e) -> T:
        pass

    @abstractmethod
    def map(self, e) -> T:
        pass

    @abstractmethod
    def range(self, e) -> T:
        pass


class Expr(ABC):
    @abstractmethod
    def visit(self, v: ExprVisitor[T]) -> T:
        pass
