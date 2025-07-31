from parser.nodes import *
from parser.nodes.stmt.base import StmtVisitor

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
        return f"{TAB * self.indent}{e.visit(self)}"

    """ stmt """

    def expr_stmt(self, e):
        return f"{e.expr.visit(self)};"

    def var_decl(self, e):
        out = []
        for decl in e.decls:
            out.append(f"{decl[0]} = {decl[1].visit(self)}")
        return f"var {', '.join(out)};"

    def if_stmt(self, e):
        pass

    def while_stmt(self, e):
        pass

    def loop_flow(self, e):
        pass

    def ret_stmt(self, e):
        pass

    def function(self, e):
        pass

    def use_stmt(self, e):
        pass

    def block_stmt(self, e):
        self.indent += 1
        out = ""
        for stmt in e.stmts:
            out += self.eval_stmt(stmt)
        self.indent -= 1

        t = TAB * self.indent
        return f"{{\n{out}\n{t}}}"

    """ expr """

    def assign(self, e: "Assign"):
        return f"{e.name.data} = {self.eval_expr(e.value)}"

    def binary(self, e: "Binary"):
        return f"{self.eval_expr(e.left)} {e.op.ttype.value} {self.eval_expr(e.right)}"

    def grouping(self, e: "Grouping"):
        return f"({self.eval_expr(e.expr)})"

    def literal(self, e: "LiteralVal"):
        return f"{e.val.to_string()}"

    def unary(self, e: "Unary"):
        return f"{e.op}{self.eval_expr(e.expr)}"

    def variable(self, e: "Variable"):
        return f"{e.name.data}"

    def block_expr(self, e: "BlockExpr"):
        self.indent += 1
        out = ""
        for stmt in e.stmts:
            out += self.eval_stmt(stmt)
        self.indent -= 1

        t = "\t" * self.indent
        return f"{{\n{out}\n{t}}}"

    def logical(self, e: "Logical"):
        return f"{self.eval_expr(e.left)} {e.op.ttype} {self.eval_expr(e.right)}"

    def ternary(self, e: "Ternary"):
        return f"{self.eval_expr(e.cond)} ? {self.eval_expr(e.if_true)} : {self.eval_expr(e.if_false)}"

    def call(self, e: "Call"):
        return ""
        # return f"{self.eval(e.func)}({', '.join(map(self.eval, e.args))})"

    def if_expr(self, e: "IfExpr"):
        return ""
        # return f"if {self.eval(e.cond)} {{ {self.eval(e.block)} }} {elsifs if e.elsifs else ''}{els if e.els else ''}"

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
