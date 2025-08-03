from error.error import LoopBreak, LoopContinue
from interpreter.environment import Environment
from parser.nodes.expr.base import Expr, ExprVisitor
from parser.nodes.stmt.base import Stmt, StmtVisitor

from tokens import TType

from eotypes import *

from parser.nodes.expr.node import *
from parser.nodes.stmt.node import *


class Interpreter(ExprVisitor[Type], StmtVisitor):
    env: Environment

    def __init__(self, tree: list[Stmt]):  # expr for now
        self.trees = tree
        self.globals = Environment()
        self.env = self.globals

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
        for name, expr in e.decls:
            self.env.define(name, self.eval_expr(expr))

    def block_stmt(self, e: BlockStmt):
        self.eval_block(e.stmts)

    def if_stmt(self, e: IfStmt):
        raise Exception()

    def while_stmt(self, e: WhileStmt):
        while self.is_truthy(self.eval_expr(e.cond)):
            try:
                self.eval_block(e.block)
            except LoopBreak:
                break
            except LoopContinue:
                pass

    def for_stmt(self, e: ForStmt):
        raise Exception()

    def loop_flow(self, e: LoopFlow):
        match e.type:
            case "break":
                raise LoopBreak()
            case "continue":
                raise LoopContinue()

    def ret_stmt(self, e: RetStmt):
        raise Exception()

    def function(self, e: Function):
        raise Exception()

    def use_stmt(self, e: UseStmt):
        raise Exception()

    """ Expr """

    def assign(self, e: Assign):

        return Nil()

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
        raise Exception()

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
        raise Exception()

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

    """ Util """

    def eval_block(self, stmts: list[Stmt], env: Environment | None = None):
        """Pass in an `env` because for functions, they need to declare their parameters"""
        prev = self.env
        try:  # for 'return', 'break' etc.
            self.env = env if env != None else Environment(prev)
            out: Type = Nil()
            for stmt in stmts:
                if isinstance(stmt, ExprStmt):
                    out = self.eval_expr(stmt.expr)
        finally:
            self.env = prev

        return out

    def is_truthy(self, val: Type):
        if val.val == None:
            return False
        if val.tname == "bool":
            return val.val
        return True
