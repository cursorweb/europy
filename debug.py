from parser.nodes import *

TAB = "    "


# quick debug
class Printer(ExprVisitor[str], StmtVisitor[str]):
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

    def fn_decl(self, e):
        opt_params = ", " if len(e.params) and len(e.opt_params) else ""
        opt_params += ", ".join(
            [f"{name.data} = {self.eval_expr(expr)}" for name, expr in e.opt_params]
        )
        return f"fn {e.name.data}({', '.join([tok.data for tok in e.params])}{opt_params}) {self.print_block(e.block)}"

    def use_stmt(self, e):
        raise Exception()

    """ expr like """

    def if_expr(self, e: "IfExpr"):
        out = f"if {self.eval_expr(e.cond)} {self.print_block(e.if_true)}"
        for cond, if_true in e.elifs:
            out += f" elif {self.eval_expr(cond)} {self.print_block(if_true)}"
        if e.els:
            out += f" else {self.print_block(e.els)}"
        return out

    def while_expr(self, e):
        return f"while {self.eval_expr(e.cond)} {self.print_block(e.block)}"

    def for_expr(self, e):
        name = e.name.data
        els = f" else {self.print_block(e.els)}" if e.els != None else ""
        return f"for {name} in {e.iter.visit(self)} {self.print_block(e.block)}{els}"

    def loop_flow(self, e):
        val = f" {self.eval_expr(e.val)}" if e.val != None else ""
        return f"{e.type}{val}"

    def return_expr(self, e):
        out = f" {self.eval_expr(e.val)}" if e.val else ""
        return f"return{out}"

    """ expr """

    def assign(self, e: "Assign"):
        return f"{self.eval_expr(e.target)} = {self.eval_expr(e.value)}"

    def binary(self, e: "Binary"):
        return f"{self.eval_expr(e.left)} {e.op.ttype.value} {self.eval_expr(e.right)}"

    def grouping(self, e: "Grouping"):
        return f"({self.eval_expr(e.expr)})"

    def literal(self, e: "LiteralVal"):
        return f"{repr(e.val)}"

    def unary(self, e: "Unary"):
        return f"{e.op.ttype.value}{self.eval_expr(e.expr)}"

    def variable(self, e: "Variable"):
        return f"{e.name.data}#{e.scope if e.scope != None else 'g'}"

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

    def get(self, e: "Get"):
        return f"{self.eval_expr(e.name)}[{self.eval_expr(e.idx)}]"

    def prop(self, e: "Prop"):
        raise Exception()

    def array(self, e: "ArrayExpr"):
        items = [self.eval_expr(itm) for itm in e.itms]
        return f"[{', '.join(items)}]"

    def map(self, e: "Map"):
        raise Exception()

    def range(self, e: "RangeExpr"):
        eq = "=" if e.inclusive else ""
        return f"{self.eval_expr(e.start)}..{eq}{self.eval_expr(e.end)}"

    def print_block(self, stmts: list[Stmt]):
        self.indent += 1
        out = ""
        for stmt in stmts:
            out += self.eval_stmt(stmt)
        self.indent -= 1

        t = TAB * self.indent
        return f"{{\n{out}{t}}}"
