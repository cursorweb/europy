from abc import ABC, abstractmethod


# things like interpreter, resolver will 'implement' this
class ExprVisitor(ABC):
    @abstractmethod
    def assign(self, e): pass

    @abstractmethod
    def binary(self, e): pass

    @abstractmethod
    def grouping(self, e): pass

    @abstractmethod
    def literal(self, e): pass

    @abstractmethod
    def unary(self, e): pass

    @abstractmethod
    def variable(self, e): pass

    @abstractmethod
    def block(self, e): pass

    @abstractmethod
    def logical(self, e): pass

    @abstractmethod
    def ternary(self, e): pass

    @abstractmethod
    def call(self, e): pass

    @abstractmethod
    def if_expr(self, e): pass

    @abstractmethod
    def get(self, e): pass

    @abstractmethod
    def set(self, e): pass

    @abstractmethod
    def prop(self, e): pass

    @abstractmethod
    def array(self, e): pass

    @abstractmethod
    def map(self, e): pass

    @abstractmethod
    def range(self, e): pass

class Expr(ABC):
    @abstractmethod
    def visit(self, v: ExprVisitor): pass