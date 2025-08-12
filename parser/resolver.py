from error.error import EoSyntaxError
from parser.nodes.expr.base import Expr, ExprVisitor
from parser.nodes.stmt.base import Stmt, StmtVisitor

from parser.nodes.expr.node import *
from parser.nodes.stmt.node import *


# TODO: in order to add shadowing, we are going to need to upgrade the resolver
class Resolver(ExprVisitor, StmtVisitor):
    scopes: list[dict[str, bool]]

    def __init__(self, trees: list[Stmt]):
        self.trees = trees
        self.fn_depth = 0
        """
        We use depth instead of a `bool` because of this code example:
        ```
        fn a() {           // self.in_fn = True
            fn b() {       // self.in_fn = True
                return 1;
            }              // self.in_fn = False
            return 2;      // <-- Error?!
        }
        ```
        Also, this exists in resolver in general because it's considered a *syntax error*,
        and we want to catch as many of those as possible before runtime
        (e.g. don't make Break an error that while loops implicitly catch)
        """
        self.loop_depth = 0
        self.scopes = []

    def run(self) -> list[EoSyntaxError]:
        errs = []
        for tree in self.trees:
            try:
                self.rstmt(tree)
            except EoSyntaxError as e:
                errs.append(e)

        return errs

    """ Resolve utils """

    def rstmt(self, node: Stmt):
        node.visit(self)

    def rexpr(self, node: Expr):
        node.visit(self)

    def rblock(self, nodes: list[Stmt], start_scope=True):
        if start_scope:
            self.begin_scope()
        for node in nodes:
            self.rstmt(node)
        if start_scope:
            self.end_scope()

    def resolve_var(self, tok: Token, expr: Variable | Assign):
        name = tok.data
        for i, scope in enumerate(reversed(self.scopes)):
            if name in scope and scope[name]:
                expr.scope = i
                return

    def begin_scope(self):
        self.scopes.append({})

    def top(self):
        return self.scopes[-1]

    def end_scope(self):
        self.scopes.pop()

    def declare(self, var: str):
        """Declare variable without giving it a value"""
        if len(self.scopes):
            self.top()[var] = False

    def define(self, var: str):
        if len(self.scopes):
            self.top()[var] = True

    """ Stmt """

    def expr_stmt(self, e: ExprStmt):
        return self.rexpr(e.expr)

    def var_decl(self, e: VarDecl):
        for name, val in e.decls:
            self.declare(name)
            self.rexpr(val)
            self.define(name)

    def if_expr(self, e: IfExpr):
        self.rexpr(e.cond)
        self.rblock(e.if_true)
        for cond, if_true in e.elifs:
            self.rexpr(cond)
            self.rblock(if_true)
        if e.els:
            self.rblock(e.els)

    def while_expr(self, e: WhileExpr):
        self.rexpr(e.cond)
        self.loop_depth += 1
        self.rblock(e.block)
        self.loop_depth -= 1

    def for_expr(self, e: ForExpr):
        raise Exception()

    def loop_flow(self, e: LoopFlow):
        if self.loop_depth == 0:
            raise EoSyntaxError(
                e.token.lf, f"{e.type} statements can only be used inside loops"
            )

    def return_expr(self, e: ReturnExpr):
        if self.fn_depth == 0:
            raise EoSyntaxError(
                e.token.lf, "Return statements can only be inside functions"
            )

        if e.val:
            self.rexpr(e.val)

    def fn_decl(self, e: FunctionDecl):
        self.declare(e.name.data)
        self.define(e.name.data)

        seen_names = set()

        self.begin_scope()
        for token in e.params:
            name = token.data

            if name in seen_names:
                raise EoSyntaxError(token.lf, f"Duplicate parameter '{name}'.")
            seen_names.add(name)

            self.declare(name)
            self.define(name)

        for token, expr in e.opt_params:
            name = token.data

            if name in seen_names:
                raise EoSyntaxError(token.lf, f"Duplicate parameter '{name}'.")
            seen_names.add(name)

            self.declare(name)
            self.rexpr(expr)
            self.define(name)

        self.fn_depth += 1
        self.rblock(e.block, False)
        self.fn_depth -= 1
        self.end_scope()

    def use_stmt(self, e: UseStmt):
        raise Exception()

    """ Expr """

    def assign(self, e: Assign):
        self.resolve_var(e.name, e)
        self.rexpr(e.value)

    def binary(self, e: Binary):
        self.rexpr(e.left)
        self.rexpr(e.right)

    def grouping(self, e: Grouping):
        self.rexpr(e.expr)

    def literal(self, e: LiteralVal):
        return

    def unary(self, e: Unary):
        self.rexpr(e.expr)

    def variable(self, e: Variable):
        name = e.name.data
        if len(self.scopes) and name in self.top() and not self.top()[name]:
            raise EoSyntaxError(
                e.name.lf, "Variable can't refer to itself in declaration"
            )

        self.resolve_var(e.name, e)

    def block_expr(self, e: BlockExpr):
        self.rblock(e.stmts)

    def logical(self, e: Logical):
        self.rexpr(e.left)
        self.rexpr(e.right)

    def call(self, e: Call):
        self.rexpr(e.func)
        for arg in e.args:
            self.rexpr(arg)
        for _, arg in e.named_args:
            self.rexpr(arg)

    def get(self, e: Get):
        raise Exception()

    def set(self, e: Set):
        raise Exception()

    def prop(self, e: Prop):
        raise Exception()

    def array(self, e: ArrayExpr):
        for itm in e.itms:
            self.rexpr(itm)

    def map(self, e: Map):
        raise Exception()

    def range(self, e: Range):
        raise Exception()
