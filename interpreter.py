from parser.nodes.expr.base import Expr, ExprVisitor
from parser.nodes.stmt.base import Stmt, StmtVisitor

from eotypes import Type

from parser.nodes.expr.node import *
from parser.nodes.stmt.node import *


class Interpreter(ExprVisitor):
    def __init__(self, tree: Expr): # expr for now
        self.trees = tree
    
    def run(self):
        return self.eval_expr(self.trees)
    

    """ Evals """
    def eval_expr(self, e: Expr) -> Type:
        return e.visit(self)
    

    """ Stmt """



    """ Expr """
    def assign(self, e: 'Assign'): pass

    def binary(self, e: 'Binary'):
        left = self.eval_expr(e.left)
        right = self.eval_expr(e.right)

        return left.binary(e.op, right)

    def grouping(self, e: 'Grouping'):
        return self.eval_expr(e.expr)
    
    def literal(self, e: 'Literal'):
        return e.val
    
    def unary(self, e: 'Unary'):
        right = self.eval_expr(e.expr)
        return right.unary(e.op)

    def variable(self, e: 'Variable'): pass

    def block(self, e: 'Block'): pass

    def logical(self, e: 'Logical'): pass

    def ternary(self, e: 'Ternary'): pass

    def call(self, e: 'Call'): pass

    def if_expr(self, e: 'IfExpr'): pass

    def get(self, e: 'Get'): pass

    def set(self, e: 'Set'): pass

    def prop(self, e: 'Prop'): pass

    def array(self, e: 'Array'): pass

    def map(self, e: 'Map'): pass
    
    def range(self, e: 'Range'): pass