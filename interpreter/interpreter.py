from typing import Iterable

from eotypes.callable import Callable, EoFunction, make_fn
from error.error import EoTypeError, EoErrorResult, FnReturn, LoopBreak, LoopContinue
from interpreter.environment import Environment
from parser.nodes.expr.base import Expr, ExprVisitor
from parser.nodes.stmt.base import Stmt, StmtVisitor

from tokens import TType

from eotypes import *

from parser.nodes.expr.node import *
from parser.nodes.stmt.node import *

import time


class Interpreter(ExprVisitor[Type], StmtVisitor):
    env: Environment

    def __init__(self, tree: list[Stmt]):  # expr for now
        self.trees = tree
        self.globals = Environment()
        self.env = self.globals
        """
        Note how we need both globals end env.
        If we just had env, which I think the old rust version had,
        the problem would have become that when you become nested, the resolver wants you to look globally.
        But there is no global, and so you'd just keep looking in your current environment/keep backtracking to your parent environment.
        That'll still get you the same error or something else entirely.
        """

        def print_fn(dict: dict[str, Type]):
            print(dict["name"].to_string())
            return Nil()

        def clock_fn(dict: dict[str, Type]):
            # measure time in milliseconds
            return Num(time.perf_counter_ns() / 1_000_000)

        self.globals.define("print", make_fn(["name"], [], print_fn))
        self.globals.define("println", make_fn(["name"], [], print_fn))
        self.globals.define("clock", make_fn([], [], clock_fn))

    def run(self):
        for tree in self.trees:
            self.eval_stmt(tree)

    """ Evals """

    def eval_stmt(self, e: Stmt):
        e.visit(self)

    def eval_expr(self, e: Expr) -> Type:
        return e.visit(self)

    """ Stmt """

    def expr_stmt(self, e: ExprStmt):
        self.eval_expr(e.expr)

    def var_decl(self, e: VarDecl):
        for name, expr in e.decls:
            self.env.define(name, self.eval_expr(expr))

    """ Expr like """

    def if_expr(self, e: IfExpr):
        if self.is_truthy(self.eval_expr(e.cond)):
            return self.eval_block(e.if_true)

        for cond, if_true in e.elifs:
            if self.is_truthy(self.eval_expr(cond)):
                return self.eval_block(if_true)

        if e.els:
            return self.eval_block(e.els)

        return Nil()

    def while_expr(self, e: WhileExpr) -> Type:
        out: Type = Nil()

        while self.is_truthy(self.eval_expr(e.cond)):
            try:
                out = self.eval_block(e.block)
            except LoopBreak as v:
                return v.val
            except LoopContinue:
                pass

        return out

    def for_expr(self, e: ForExpr) -> Type:
        # TODO: what are iterators?
        name = e.name.data

        iter_type = self.eval_expr(e.iter)
        if not isinstance(iter_type, (Array, Range)):
            raise EoTypeError(e.name.lf, "Only arrays can be iterated on")

        iter: Iterable[int | Type]

        if isinstance(iter_type, Range):
            end = iter_type.end
            if iter_type.inclusive:
                end += 1

            iter = range(int(iter_type.start), int(end))
        else:
            iter = iter_type.val

        out: Type = Nil()

        for itm in iter:
            try:
                env = Environment(self.env)
                if isinstance(itm, int):
                    itm = Num(itm)
                env.define(name, itm)
                out = self.eval_block(e.block, env)
            except LoopBreak as v:
                return v.val
            except LoopContinue:
                pass

        if e.els:
            # this code would only run if the above block
            # didn't throw a "control flow"
            out = self.eval_block(e.els)

        return out

    def loop_flow(self, e: LoopFlow) -> Type:
        match e.type:
            case "break":
                if e.val:
                    val = self.eval_expr(e.val)
                else:
                    val = Nil()
                raise LoopBreak(val)
            case "continue":
                raise LoopContinue()
            case _:
                raise Exception("Unreachable code")

    def return_expr(self, e: ReturnExpr) -> Type:
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

    def assign(self, e: Assign) -> Type:
        value = self.eval_expr(e.value)

        if isinstance(e.lval, Variable):
            var = e.lval
            if var.scope != None:
                self.env.assign_at(var.name, value, var.scope)
            else:
                self.globals.assign(var.name, value)
        elif isinstance(e.target, Get):
            try:
                target = self.eval_expr(e.target.name)
                idx = self.eval_expr(e.target.idx)

                target.set(idx, value)
            except EoErrorResult as err:
                raise err.with_lf(e.target.brack)

        return Nil()

    def binary(self, e: Binary) -> Type:
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
                    return left.nequals(right)
                case TType.Greater:
                    return left.grtr(right)
                case TType.Less:
                    return left.less(right)
                case TType.GreaterEq:
                    return left.grtre(right)
                case TType.LessEq:
                    return left.lesse(right)
                case _:
                    raise Exception("Unreachable")
        except EoErrorResult as err:
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

    def logical(self, e: Logical) -> Type:
        lval = self.eval_expr(e.left)

        if e.op.ttype == TType.Or:
            if self.is_truthy(lval):
                return lval
        else:  # and
            if not self.is_truthy(lval):
                return lval

        return self.eval_expr(e.right)

    def call(self, e: Call) -> Type:
        callee = self.eval_expr(e.func)

        if not isinstance(callee, Callable):
            raise EoTypeError(e.paren.lf, "Invalid call target.")

        args = [self.eval_expr(expr) for expr in e.args]
        named_args: dict[str, Type] = dict(
            (token.data, self.eval_expr(expr)) for token, expr in e.named_args
        )

        return callee.call(e.paren, args, named_args)

    def get(self, e: Get):
        try:
            name = self.eval_expr(e.name)
            idx = self.eval_expr(e.idx)
            return name.get(idx)
        except EoErrorResult as err:
            raise err.with_lf(e.brack)

    def prop(self, e: Prop):
        val = self.eval_expr(e.val)
        name = e.name.data

        try:
            return val.prop(name)
        except EoErrorResult as err:
            raise err.with_lf(e.name)

    def array(self, e: ArrayExpr):
        items = []
        for itm in e.itms:
            # we have an AMAZING opportunity to be lazy here
            items.append(itm.visit(self))
        return Array(items)

    def map(self, e: MapExpr):
        out = {}

        for k, v in e.itms:
            key = self.eval_expr(k)
            value = self.eval_expr(v)

            out[Map.key(key)] = value

        return Map(out)

    def range(self, e: RangeExpr):
        inclusive = e.dot.ttype == TType.DotEq
        start = self.eval_expr(e.start)
        end = self.eval_expr(e.end)

        if start.tname != "num" or end.tname != "num":
            raise EoTypeError(e.dot.lf, "Ranges can only have numbers")

        return Range(start.val, end.val, inclusive)

    """ Util """

    def eval_block(self, stmts: list[Stmt], env: Environment | None = None) -> Type:
        """Pass in an `env` because for functions, they need to declare their parameters"""
        prev = self.env
        try:  # for 'return', 'break' etc.
            self.env = env if env != None else Environment(prev)
            out: Type = Nil()
            for stmt in stmts:
                if isinstance(stmt, ExprStmt):
                    # TODO: optimization, last expr is the value, once everything is an "expression"
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
