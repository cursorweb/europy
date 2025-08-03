from typing import cast

from parser.nodes import *

TAB = "    "


# quick debug
class Printer(ExprVisitor, StmtVisitor):
    def __init__(self, tree: Stmt) -> None:
        self.tree = tree
        self.indent = 0

    def run(self):
        return self.eval_stmt(self.tree)

    def eval_expr(self, e: Expr) -> str:
        return e.visit(self)

    def eval_stmt(self, e: Stmt) -> str:
        return f"{TAB * self.indent}{e.visit(self)}\n"

    """ stmt """

    def expr_stmt(self, e):
        return f"{e.expr.visit(self)};"

    def var_decl(self, e):
        out = []
        for decl in e.decls:
            out.append(f"{decl[0]} = {decl[1].visit(self)}")
        return f"var {', '.join(out)};"

    def if_stmt(self, e: "IfStmt"):
        out = f"if {self.eval_expr(e.cond)} {self.print_block(e.if_true)}"
        for cond, if_true in e.elifs:
            out += f" elif {self.eval_expr(cond)} {self.print_block(if_true)}"
        if e.els:
            out += f" else {self.print_block(e.els)}"
        return out

    def while_stmt(self, e):
        return f"while {self.eval_expr(e.cond)} {self.print_block(e.block)}"

    def for_stmt(self, e):
        pass

    def loop_flow(self, e):
        return f"{e.type};"

    def return_stmt(self, e):
        out = f" {self.eval_expr(e.val)}" if e.val else ""
        return f"return{out};"

    def fn_decl(self, e):
        opt_params = ", " if len(e.params) and len(e.opt_params) else ""
        opt_params += ", ".join(
            [f"{name.data} = {self.eval_expr(expr)}" for name, expr in e.opt_params]
        )
        return f"fn {e.name.data}({', '.join([tok.data for tok in e.params])}{opt_params}) {self.print_block(e.block)}"

    def use_stmt(self, e):
        pass

    def block_stmt(self, e):
        return f"{self.print_block(e.stmts)}"

    """ expr """

    def assign(self, e: "Assign"):
        return f"{e.name.data}#{e.scope} = {self.eval_expr(e.value)}"

    def binary(self, e: "Binary"):
        return f"{self.eval_expr(e.left)} {e.op.ttype.value} {self.eval_expr(e.right)}"

    def grouping(self, e: "Grouping"):
        return f"({self.eval_expr(e.expr)})"

    def literal(self, e: "LiteralVal"):
        return f"{repr(e.val)}"

    def unary(self, e: "Unary"):
        return f"{e.op}{self.eval_expr(e.expr)}"

    def variable(self, e: "Variable"):
        return f"{e.name.data}#{e.scope}"

    def block_expr(self, e: "BlockExpr"):
        return self.print_block(e.stmts)

    def logical(self, e: "Logical"):
        return f"{self.eval_expr(e.left)} {e.op.ttype.value} {self.eval_expr(e.right)}"

    def call(self, e: "Call"):
        args = ", ".join([self.eval_expr(arg) for arg in e.args])
        named_args = ", " if len(e.named_args) and len(e.args) else ""
        named_args += ", ".join(
            [f"{tok.data} = {self.eval_expr(arg)}" for tok, arg in e.named_args]
        )
        return f"{self.eval_expr(e.func)}({args}{named_args})"

    def if_expr(self, e: "IfExpr"):
        return self.if_stmt(cast(IfStmt, e))

    def get(self, e: "Get"):
        pass

    def set(self, e: "Set"):
        pass

    def prop(self, e: "Prop"):
        pass

    def array(self, e: "Array"):
        pass

    def map(self, e: "Map"):
        pass

    def range(self, e: "Range"):
        pass

    def print_block(self, stmts: list[Stmt]):
        self.indent += 1
        out = ""
        for stmt in stmts:
            out += self.eval_stmt(stmt)
        self.indent -= 1

        t = TAB * self.indent
        return f"{{\n{out}{t}}}"
