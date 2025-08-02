from parser.nodes.expr.base import ExprVisitor
from parser.nodes.stmt.base import StmtVisitor


class Resolver(ExprVisitor, StmtVisitor):
    pass
