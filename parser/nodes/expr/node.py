from eotypes.type import Type
from .base import Expr
from ..stmt.node import Stmt
from tokens import Token


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


class Variable(Expr):
    def __init__(self, name: Token):
        self.name = name

    def visit(self, v):
        return v.variable(self)


class Block(Expr):
    def __init__(self, stmts: Stmt):
        self.stmts = stmts

    def visit(self, v):
        return v.block(self)

# and/or


class Logical(Expr):
    def __init__(self, l: Expr, op: Token, r: Expr):
        self.left = l
        self.op = op
        self.right = r

    def visit(self, v):
        return v.logical(self)


class Ternary(Expr):
    def __init__(self, c: Expr, t: Expr, f: Expr):
        self.cond = c
        self.if_true = t
        self.if_false = f

    def visit(self, v):
        return v.ternary(self)


class Call(Expr):
    def __init__(self, func: Expr, paren: Token, args: list[Expr]):
        self.func = func
        self.paren = paren
        self.args = args

    def visit(self, v):
        return v.call(self)


class IfExpr(Expr):
    def __init__(self, cond: Expr, block: list[Stmt], elsifs: list[(Expr, list[Stmt])], els: list[Stmt] = None):
        self.cond = cond
        self.block = block
        self.elsifs = elsifs
        self.els = els

    def visit(self, v):
        return v.if_expr(self)


class Get(Expr):
    # expr[expr]
    def __init__(self, expr: Expr, brack: Token, name: Expr):
        self.expr = expr
        self.brack = brack
        self.name = name

    def visit(self, v):
        return v.get(self)


class Set(Expr):
    # expr[expr] = expr
    def __init__(self, expr: Expr, brack: Token, name: Expr, val: Expr):
        self.expr = expr
        self.brack = brack
        self.name = name
        self.val = val

    def visit(self, v):
        return v.set(self)

# <mod>.<func>


class Prop(Expr):
    def __init__(self, mod: Expr, name: Token):
        self.mod = mod
        self.name = name

    def visit(self, v):
        return v.prop(self)


class Array(Expr):
    def __init__(self, itms: list[Expr]):
        self.itms = itms

    def visit(self, v):
        return v.array(self)


class Map(Expr):
    def __init__(self, itms: list[(Expr, Expr)]):
        self.itms = itms

    def visit(self, v):
        return v.map(self)


class Range(Expr):
    # 1..3 | 1.=4
    def __init__(self, s: Expr, dot: Token, e: Expr, inc: bool):
        self.start = s
        self.dot = dot
        self.end = e
        self.inc = inc

    def visit(self, v):
        return v.range(self)
