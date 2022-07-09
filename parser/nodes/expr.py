from abc import ABC, abstractmethod

from eotypes.type import Type
from tokens import Token


# things like interpreter, resolver will 'implement' this
class ExprVisitor(ABC):
    @abstractmethod
    def assign(e: 'Assign'): pass

    @abstractmethod
    def binary(e: 'Binary'): pass

    @abstractmethod
    def grouping(e: 'Grouping'): pass

    @abstractmethod
    def literal(e: 'Literal'): pass

    @abstractmethod
    def unary(e: 'Unary'): pass

    @abstractmethod
    def unary(e: 'Unary'): pass

    @abstractmethod
    def variable(e: 'Variable'): pass

    @abstractmethod
    def block(e: 'Block'): pass

    @abstractmethod
    def logical(e: 'Logical'): pass

    @abstractmethod
    def ternary(e: 'Ternary'): pass

    @abstractmethod
    def call(e: 'Call'): pass

    @abstractmethod
    def if_expr(e: 'IfExpr'): pass

    @abstractmethod
    def get(e: 'Get'): pass

    @abstractmethod
    def set(e: 'Set'): pass

    @abstractmethod
    def prop(e: 'Prop'): pass

    @abstractmethod
    def array(e: 'Array'): pass

    @abstractmethod
    def map(e: 'Map'): pass
    
    @abstractmethod
    def range(e: 'Range'): pass


class Expr(ABC):
    @abstractmethod
    def visit(self, v: ExprVisitor): pass


class Assign(Expr):
    def __init__(self, name: Token, value: Expr):
        self.name = name
        self.value = value

    def visit(self, v):
        return v.assign(self)


class Binary(Expr):
    def __init__(self, l: Expr, o: Token, r: Expr):
        self.left = l
        self.op = o
        self.right = r

    def visit(self, v):
        return v.binary(self)


class Grouping(Expr):
    def __init__(self, expr: Expr):
        self.expr = expr

    def visit(self, v):
        return v.grouping(self)


class Literal(Expr):
    def __init__(self, val: Type):
        self.val = val

    def visit(self, v):
        return v.literal(self)


class Unary(Expr):
    def __init__(self, op: Token, expr: Expr):
        self.op = op
        self.expr = expr

    def visit(self, v):
        return v.unary(self)
