from parser.nodes.expr.base import Expr, ExprVisitor
from parser.nodes.stmt.base import Stmt, StmtVisitor

from eotypes import Type

from parser.nodes.expr.node import *
from parser.nodes.stmt.node import *


class Interpreter(ExprVisitor, StmtVisitor):
    def __init__(self, tree: list[Stmt]):  # expr for now
        self.trees = tree

    def run(self):
        for tree in self.trees:
            return self.eval_stmt(tree)

    """ Evals """

    def eval_stmt(self, e: Stmt):
        return e.visit(self)

    def eval_expr(self, e: Expr) -> Type:
        return e.visit(self)

    """ Stmt """

    def expr_stmt(self, e: ExprStmt):
        return self.eval_expr(e.expr)

    def var_decl(self, e: VarDecl):
        pass

    def block_stmt(self, e: BlockStmt):
        pass

    def if_stmt(self, e: IfStmt):
        pass

    def while_stmt(self, e: WhileStmt):
        pass

    def loop_flow(self, e: LoopFlow):
        pass

    def ret_stmt(self, e: RetStmt):
        pass

    def function(self, e: Function):
        pass

    def use_stmt(self, e: UseStmt):
        pass

    """ Expr """

    def assign(self, e: Assign):
        pass

    def binary(self, e: Binary):
        left = self.eval_expr(e.left)
        right = self.eval_expr(e.right)

        return left.binary(e.op, right)

    def grouping(self, e: Grouping):
        return self.eval_expr(e.expr)

    def literal(self, e: LiteralVal):
        return e.val

    def unary(self, e: Unary):
        right = self.eval_expr(e.expr)
        return right.unary(e.op)

    def variable(self, e: Variable):
        pass

    def block_expr(self, e: BlockExpr):
        pass

    def logical(self, e: Logical):
        pass

    def ternary(self, e: Ternary):
        pass

    def call(self, e: Call):
        pass

    def if_expr(self, e: IfExpr):
        pass

    def get(self, e: Get):
        pass

    def set(self, e: Set):
        pass

    def prop(self, e: Prop):
        pass

    def array(self, e: Array):
        pass

    def map(self, e: Map):
        pass

    def range(self, e: Range):
        pass

    """ Util """

    def is_truthy(self, val: Type):
        if val.val == None:
            return False
        if val.tname == "bool":
            return val.val
        return True
