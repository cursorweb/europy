from parser.nodes.expr.base import Expr, ExprVisitor
from parser.nodes.stmt.base import Stmt, StmtVisitor

from tokens import TType

from eotypes import *

from parser.nodes.expr.node import *
from parser.nodes.stmt.node import *


class Interpreter(ExprVisitor[Type], StmtVisitor):
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
        self.eval_block(e.stmts)

    def if_stmt(self, e: IfStmt):
        pass

    def while_stmt(self, e: WhileStmt):
        pass

    def for_stmt(self, e: ForStmt):
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
        try:
            match e.op.ttype:
                case TType.Plus:
                    return left.plus(right)
                case TType.Minus:
                    return left.minus(right)
                case TType.Times:
                    return left.times(right)
                case TType.Divide:
                    return left.divide(right)
                case TType.Mod:
                    return left.mod(right)
                case TType.Pow:
                    return left.pow(right)
                case TType.EqEq:
                    return left.equals(right)
                case TType.NotEq:
                    return not left.equals(right)
                case TType.Greater:
                    return left.grtr(right)
                case TType.Less:
                    return left.less(right)
                case TType.GreaterEq:
                    return left.grtr(right) or left.equals(right)
                case TType.LessEq:
                    return left.less(right) or left.equals(right)

        except EoTypeErrorResult as err:
            raise err.with_lf(e.op)

    def grouping(self, e: Grouping):
        return self.eval_expr(e.expr)

    def literal(self, e: LiteralVal):
        return e.val

    def unary(self, e: Unary) -> "Type":
        right = self.eval_expr(e.expr)
        match e.op.ttype:
            case TType.Minus:
                return right.negate()
            case TType.Not:
                return right.not_op()
            case _:
                raise Exception("unreachable")

    def variable(self, e: Variable):
        pass

    def block_expr(self, e: BlockExpr):
        return self.eval_block(e.stmts)

    def logical(self, e: Logical):
        lval = self.eval_expr(e.left)

        if e.op.ttype == TType.Or:
            if self.is_truthy(lval):
                return lval
        else:  # and
            if not self.is_truthy(lval):
                return lval

        self.eval_expr(e.right)

    def call(self, e: Call):
        pass

    def if_expr(self, e: IfExpr) -> Type:
        if self.is_truthy(self.eval_expr(e.cond)):
            return self.eval_block(e.if_true)

        for cond, if_true in e.elifs:
            if self.is_truthy(self.eval_expr(cond)):
                return self.eval_block(if_true)

        if e.els:
            return self.eval_block(e.els)

        return Nil()

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

    def eval_block(self, stmts: list[Stmt]):
        out: Type = Nil()
        for stmt in stmts:
            if isinstance(stmt, ExprStmt):
                out = self.eval_expr(stmt.expr)

        return out

    def is_truthy(self, val: Type):
        if val.val == None:
            return False
        if val.tname == "bool":
            return val.val
        return True
