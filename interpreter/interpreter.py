from eotypes.callable import Callable, EoFunction, make_fn
from error.error import EoTypeError, FnReturn, LoopBreak, LoopContinue
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

        def fn(dict):
            print(dict["name"].to_string())
            return Nil()

        self.globals.define("print", make_fn(["name"], [], fn))

    def run(self):
        for tree in self.trees:
            self.eval_stmt(tree)

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
        if self.is_truthy(self.eval_expr(e.cond)):
            return self.eval_block(e.if_true)

        for cond, if_true in e.elifs:
            if self.is_truthy(self.eval_expr(cond)):
                return self.eval_block(if_true)

        if e.els:
            return self.eval_block(e.els)

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

    def return_stmt(self, e: ReturnStmt):
        val = self.eval_expr(e.val) if e.val != None else Nil()
        raise FnReturn(val)

    def fn_decl(self, e: FunctionDecl):
        name = e.name.data
        params = [token.data for token in e.params]
        opt_params: list[tuple[str, Type]] = [
            (token.data, self.eval_expr(expr)) for token, expr in e.opt_params
        ]
        block = e.block

        self.env.define(name, EoFunction(name, params, opt_params, block, self))

    def use_stmt(self, e: UseStmt):
        raise Exception()

    """ Expr """

    def assign(self, e: Assign):
        value = self.eval_expr(e.value)

        if e.scope != None:
            self.env.assign_at(e.name, value, e.scope)
        else:
            self.globals.assign(e.name, value)
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
                    return left.grtre(right)
                case TType.LessEq:
                    return left.lesse(right)

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
        if e.scope != None:
            return self.env.get_at(e.name, e.scope)
        else:
            return self.globals.get(e.name)

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

    def call(self, e: Call) -> Type:
        callee = self.eval_expr(e.func)

        if not isinstance(callee, Callable):
            raise EoTypeError(e.paren.lf, "Invalid call target.")

        args = [self.eval_expr(expr) for expr in e.args]
        named_args: dict[str, Type] = dict(
            (token.data, self.eval_expr(expr)) for token, expr in e.named_args
        )

        return callee.call(e.paren, args, named_args)

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

    def eval_block(self, stmts: list[Stmt], env: Environment | None = None) -> Type:
        """Pass in an `env` because for functions, they need to declare their parameters"""
        prev = self.env
        try:  # for 'return', 'break' etc.
            self.env = env if env != None else Environment(prev)
            out: Type = Nil()
            for stmt in stmts:
                if isinstance(stmt, ExprStmt):
                    out = self.eval_expr(stmt.expr)
                else:
                    self.eval_stmt(stmt)
        finally:
            self.env = prev

        return out

    def is_truthy(self, val: Type):
        if val.val == None:
            return False
        if val.tname == "bool":
            return val.val
        return True
