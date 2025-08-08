from typing import Literal
from eotypes.type import Type
from .base import Expr, ExprVisitor
from ..stmt.node import Stmt
from tokens import Token


class BlockExpr(Expr):
    def __init__(self, stmts: list[Stmt]):
        self.stmts = stmts

    def visit(self, v: ExprVisitor):
        return v.block_expr(self)


class IfExpr(Expr):
    def __init__(
        self,
        cond: Expr,
        if_true: list[Stmt],
        elifs: list[tuple[Expr, list[Stmt]]],
        els: list[Stmt] | None = None,
    ):
        self.cond = cond
        self.if_true = if_true
        self.elifs = elifs
        self.els = els

    def visit(self, v: ExprVisitor):
        return v.if_expr(self)


class WhileExpr(Expr):
    def __init__(self, cond: Expr, loop: list[Stmt]):
        self.cond = cond
        self.block = loop

    def visit(self, v: ExprVisitor):
        return v.while_expr(self)


class ForExpr(Expr):
    def __init__(self, name: str, iterator: Expr, block: list[Stmt]) -> None:
        self.name = name
        self.iter = iterator
        self.block = block

    def visit(self, v: ExprVisitor):
        return v.for_expr(self)


class LoopFlow(Expr):
    def __init__(self, token: Token, type: Literal["break", "continue"]):
        self.token = token
        self.type = type

    def visit(self, v: ExprVisitor):
        return v.loop_flow(self)


class ReturnExpr(Expr):
    def __init__(self, ret: Token, val: Expr | None = None):
        self.token = ret
        self.val = val

    def visit(self, v: ExprVisitor):
        return v.return_expr(self)


""" Expression with operator """


class Assign(Expr):
    def __init__(self, name: Token, value: Expr):
        self.name = name
        self.value = value
        self.scope: int | None = None

    def visit(self, v: "ExprVisitor"):
        return v.assign(self)


class Binary(Expr):
    def __init__(self, l: Expr, o: Token, r: Expr):
        self.left = l
        self.op = o
        self.right = r

    def visit(self, v: "ExprVisitor"):
        return v.binary(self)


class Grouping(Expr):
    def __init__(self, expr: Expr):
        self.expr = expr

    def visit(self, v: "ExprVisitor"):
        return v.grouping(self)


class LiteralVal(Expr):
    def __init__(self, val: Type):
        self.val = val

    def visit(self, v: "ExprVisitor"):
        return v.literal(self)


class Unary(Expr):
    def __init__(self, op: Token, expr: Expr):
        self.op = op
        self.expr = expr

    def visit(self, v: "ExprVisitor"):
        return v.unary(self)


class Variable(Expr):
    def __init__(self, name: Token):
        self.name = name
        self.scope: int | None = None

    def visit(self, v: "ExprVisitor"):
        return v.variable(self)


class Logical(Expr):
    # and/or
    def __init__(self, l: Expr, op: Token, r: Expr):
        self.left = l
        self.op = op
        self.right = r

    def visit(self, v: "ExprVisitor"):
        return v.logical(self)


class Call(Expr):
    def __init__(
        self,
        func: Expr,
        paren: Token,
        args: list[Expr],
        named_args: list[tuple[Token, Expr]],
    ):
        self.func = func
        self.paren = paren
        self.args = args
        self.named_args = named_args

    def visit(self, v: "ExprVisitor"):
        return v.call(self)


class Get(Expr):
    """expr[expr]"""

    def __init__(self, expr: Expr, brack: Token, name: Expr):
        self.expr = expr
        self.brack = brack
        self.name = name

    def visit(self, v: "ExprVisitor"):
        return v.get(self)


class Set(Expr):
    """expr[expr] = expr"""

    def __init__(self, expr: Expr, brack: Token, name: Expr, val: Expr):
        self.expr = expr
        self.brack = brack
        self.name = name
        self.val = val

    def visit(self, v: "ExprVisitor"):
        return v.set(self)


class Prop(Expr):
    """`<mod>.<func>`"""

    def __init__(self, mod: Expr, name: Token):
        self.mod = mod
        self.name = name

    def visit(self, v: "ExprVisitor"):
        return v.prop(self)


class Array(Expr):
    def __init__(self, itms: list[Expr]):
        self.itms = itms

    def visit(self, v: "ExprVisitor"):
        return v.array(self)


class Map(Expr):
    def __init__(self, itms: list[tuple[Expr, Expr]]):
        self.itms = itms

    def visit(self, v: "ExprVisitor"):
        return v.map(self)


class Range(Expr):
    # 1..3 | 1.=4
    def __init__(self, s: Expr, dot: Token, e: Expr, inc: bool):
        self.start = s
        self.dot = dot
        self.end = e
        self.inc = inc

    def visit(self, v: "ExprVisitor"):
        return v.range(self)
