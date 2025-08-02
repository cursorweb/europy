from error.error import EoSyntaxError
from parser.nodes.expr.base import Expr, ExprVisitor
from parser.nodes.stmt.base import Stmt, StmtVisitor

from parser.nodes.expr.node import *
from parser.nodes.stmt.node import *


class Resolver(ExprVisitor, StmtVisitor):
    def __init__(self, trees: list[Stmt]):
        self.trees = trees
        self.in_fn = False
        self.in_loop = False

    def run(self):
        for tree in self.trees:
            return self.rstmt(tree)

    """ Resolve utils """

    def rstmt(self, node: Stmt):
        node.visit(self)

    def rexpr(self, node: Expr):
        node.visit(self)

    def resolve_block(self, nodes: list[Stmt]):
        for node in nodes:
            self.rstmt(node)

    """ Stmt """

    def expr_stmt(self, e: ExprStmt):
        return self.rexpr(e.expr)

    def var_decl(self, e: VarDecl):
        pass

    def block_stmt(self, e: BlockStmt):
        return self.resolve_block(e.stmts)

    def if_stmt(self, e: IfStmt):
        self.rexpr(e.cond)
        self.resolve_block(e.if_true)
        for cond, if_true in e.elifs:
            self.rexpr(cond)
            self.resolve_block(if_true)
        if e.els:
            self.resolve_block(e.els)

    def while_stmt(self, e: WhileStmt):
        self.rexpr(e.cond)
        self.in_loop = True
        self.resolve_block(e.block)
        self.in_loop = False

    def for_stmt(self, e: ForStmt):
        raise Exception()

    def loop_flow(self, e: LoopFlow):
        if not self.in_loop:
            raise EoSyntaxError(
                e.token.lf, f"{e.type} statements can only be used inside loops"
            )

    def ret_stmt(self, e: RetStmt):
        if not self.in_fn:
            raise EoSyntaxError(
                e.token.lf, "Return statements can only be inside functions"
            )

        if e.val:
            self.rexpr(e.val)

    def function(self, e: Function):
        for name in e.params:
            pass

        for name, expr in e.opt_params:
            self.rexpr(expr)

        self.in_fn = True
        self.resolve_block(e.block)
        self.in_fn = False

    def use_stmt(self, e: UseStmt):
        pass

    """ Expr """

    def assign(self, e: Assign):
        raise Exception()

    def binary(self, e: Binary):
        self.rexpr(e.left)
        self.rexpr(e.right)

    def grouping(self, e: Grouping):
        self.rexpr(e.expr)

    def literal(self, _: LiteralVal):
        return

    def unary(self, e: Unary):
        self.rexpr(e.expr)

    def variable(self, e: Variable):
        raise Exception()

    def block_expr(self, e: BlockExpr):
        self.resolve_block(e.stmts)

    def logical(self, e: Logical):
        self.rexpr(e.left)
        self.rexpr(e.right)

    def call(self, e: Call):
        self.rexpr(e.func)
        for arg in e.args:
            self.rexpr(arg)
        for _, arg in e.named_args:
            self.rexpr(arg)

    def if_expr(self, e: IfExpr):
        self.rexpr(e.cond)
        self.resolve_block(e.if_true)
        for cond, if_true in e.elifs:
            self.rexpr(cond)
            self.resolve_block(if_true)
        if e.els:
            self.resolve_block(e.els)

    def get(self, e: Get):
        raise Exception()

    def set(self, e: Set):
        raise Exception()

    def prop(self, e: Prop):
        raise Exception()

    def array(self, e: Array):
        raise Exception()

    def map(self, e: Map):
        raise Exception()

    def range(self, e: Range):
        raise Exception()
