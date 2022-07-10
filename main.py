from lexer import Lexer
from parser import Parser
from interpreter import Interpreter
from parser.nodes.exprn import *
from tokens import TType

from error import EoError

lexer = Lexer.from_file('test/playground.eo')
tokens = None

try:
    tokens = lexer.run()
except EoError as e:
    e.display()

parser = Parser(tokens)

try:
    tree = parser.run()
except EoError as e:
    e.display()

# quick debug
class Printer(ExprVisitor):
    def __init__(self, tree: Expr) -> None:
        self.tree = tree

    def run(self):
        return self.eval(self.tree)

    def eval(self, e: Expr):
        return e.visit(self)


    def assign(self, e: 'Assign'):
        return f"{e.name.data} = {self.eval(e.value)}"
    
    def binary(self, e: 'Binary'):
        return f"{self.eval(e.left)} {e.op.ttype} {self.eval(e.right)}"

    def grouping(self, e: 'Grouping'):
        return f"({self.eval(e.expr)})"

    def literal(self, e: 'Literal'):
        return f"{e.val.to_string()}"

    def unary(self, e: 'Unary'):
        return f"{e.op}{self.eval(e.expr)}"

    def variable(self, e: 'Variable'):
        return f"{e.name.data}"

    def block(self, e: 'Block'):
        return f"{{{e.stmts}}}" # <-- todo hehehe

    def logical(self, e: 'Logical'):
        return f"{self.eval(e.left)} {e.op.ttype} {self.eval(e.right)}"

    def ternary(self, e: 'Ternary'):
        return f"{self.eval(e.cond)} ? {self.eval(e.if_true)} : {self.eval(e.if_false)}"

    def call(self, e: 'Call'):
        return f"{self.eval(e.func)}({', '.join(map(self.eval, e.args))})"

    def if_expr(self, e: 'IfExpr'):
        # todo heeheehehehe
        elsifs = map()
        els = map()
        return f"if {self.eval(e.cond)} {self.eval(e.block)}{elsifs if e.elsifs else ''}{els if e.els else ''}"

    def get(self, e: 'Get'): pass

    def set(self, e: 'Set'): pass

    def prop(self, e: 'Prop'): pass

    def array(self, e: 'Array'): pass

    def map(self, e: 'Map'): pass
    
    def range(self, e: 'Range'): pass


print(Printer(tree).run())