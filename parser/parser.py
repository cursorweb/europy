import eotypes
from error.error import EoSyntaxError

from parser.nodes.expr.base import Expr as ExprT
import parser.nodes.expr.node as Expr

from parser.nodes.stmt.base import Stmt as StmtT
import parser.nodes.stmt.node as Stmt

from tokens import TType, Token


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.i = 0

    def run(self) -> list[StmtT]:
        stmts = []

        while not self.is_end():
            stmts.append(self.stmt())

        return stmts

    """ - AST - """
    """ Stmt """

    def stmt(self) -> StmtT:
        if self.match(TType.If):
            return self.if_stmt()

        if self.match(TType.Var):
            return self.var_decl()

        if self.match(TType.While):
            return self.while_stmt()

        if self.match(TType.Do):
            return self.dowhile_stmt()

        if self.match(TType.LeftBrace):
            return Stmt.BlockStmt(self.block())

        if self.match(TType.Break, TType.Continue, TType.Return):
            return self.controlflow_stmt()

        if self.match(TType.Fn):
            pass

        if self.match(TType.Use):
            pass

        return self.expr_stmt()

    def if_stmt(self) -> StmtT:
        cond = self.expr()
        self.consume(TType.LeftBrace, "Expected '{' after if statement condition.")
        true_br = self.block()
        elif_brs = []
        else_br = None

        if self.match(TType.Elif):
            while True:
                elif_cond = self.expr()
                self.consume(
                    TType.LeftBrace, "Expected '{' after elif statement condition."
                )
                elif_brs.append((elif_cond, self.block()))
                if self.match(TType.Elif):
                    break

        if self.match(TType.Else):
            self.consume(TType.LeftBrace, "Expected '{' after else keyword.")
            else_br = self.block()

        return Stmt.IfStmt(cond, true_br, elif_brs, else_br)

    def var_decl(self) -> StmtT:
        vars: list[tuple[str, ExprT]] = []

        while True:
            name = self.next()
            if name.ttype == TType.Identifier:
                val = None

                if self.match(TType.Eq):
                    val = self.expr()
                else:
                    val = Expr.LiteralVal(eotypes.Nil())

                vars.append((name.data, val))

                if self.match(TType.Semi):
                    break
                elif self.match(TType.Comma):
                    continue
                else:
                    raise EoSyntaxError(
                        self.prev().lf,
                        "Expected ',' or ';' after variable declaration.",
                    )
            else:
                raise EoSyntaxError(self.prev().lf, "Expected variable name.")

        return Stmt.VarDecl(vars)

    def while_stmt(self) -> StmtT:
        cond = self.expr()
        self.consume(TType.LeftBrace, "Expected '{' after while loop condition.")
        body = self.block()

        return Stmt.WhileStmt(cond, body)

    def dowhile_stmt(self) -> StmtT:
        self.consume(TType.LeftBrace, "Expected '{' after do keyword.")
        body = self.block()
        self.consume(TType.While, "Expected 'while' after do loop body.")
        cond = self.expr()
        self.consume(TType.Semi, "Expected ';' after do while loop condition.")

        return Stmt.BlockStmt([Stmt.BlockStmt(body), Stmt.WhileStmt(cond, body)])

    def block(self) -> list[StmtT]:
        stmts = []

        while not self.check(TType.RightBrace) and not self.is_end():
            stmts.append(self.stmt())

        self.consume(TType.RightBrace, "Expected '}' after block expression.")

        return stmts

    def controlflow_stmt(self) -> StmtT:
        tok = self.prev()

        if tok.ttype == TType.Break:
            return Stmt.LoopFlow("break")
        elif tok.ttype == TType.Continue:
            return Stmt.LoopFlow("continue")
        elif tok.ttype == TType.Return:
            val = None
            if self.get(TType.Semi):
                val = self.expr()
            return Stmt.RetStmt(val)

        raise Exception("unreachable")

    def expr_stmt(self) -> StmtT:
        expr = self.expr()

        if not self.match(TType.Semi):
            semi = self.peek()
            # feature: last statement doesn't need semi (repl purposes probably)
            if semi.ttype != TType.RightBrace and semi.ttype != TType.EOF:
                raise EoSyntaxError(semi.lf, "Expected ';' after statement.")

        return Stmt.ExprStmt(expr)

    """ Expr """

    def expr(self) -> ExprT:
        return self.equality()

    def equality(self) -> ExprT:
        expr = self.comp()

        while self.match(TType.NotEq, TType.EqEq):
            op = self.prev()
            right = self.comp()
            expr = Expr.Binary(expr, op, right)

        return expr

    def comp(self) -> ExprT:
        expr = self.add()

        while self.match(TType.Less, TType.LessEq, TType.Greater, TType.GreaterEq):
            op = self.prev()
            right = self.add()
            expr = Expr.Binary(expr, op, right)

        return expr

    def add(self) -> ExprT:
        expr = self.mult()

        while self.match(TType.Plus, TType.Minus):
            op = self.prev()
            right = self.mult()
            expr = Expr.Binary(expr, op, right)

        return expr

    def mult(self) -> ExprT:
        expr = self.unary()

        while self.match(TType.Times, TType.Divide, TType.Mod):
            op = self.prev()
            right = self.unary()
            expr = Expr.Binary(expr, op, right)

        return expr

    def unary(self) -> ExprT:
        if self.match(TType.Not, TType.Minus):
            op = self.prev()
            right = self.unary()
            return Expr.Unary(op, right)

        return self.primary()

    def primary(self) -> ExprT:
        if self.match(TType.T_True):
            return Expr.LiteralVal(eotypes.Bool(True))
        if self.match(TType.T_False):
            return Expr.LiteralVal(eotypes.Bool(False))
        if self.match(TType.Nil):
            return Expr.LiteralVal(eotypes.Nil())

        if self.match(TType.Number, TType.String):
            t = self.prev()
            if t.ttype == TType.String:
                return Expr.LiteralVal(eotypes.String(t.data))
            else:
                return Expr.LiteralVal(eotypes.Num(t.data))

        if self.match(TType.LeftParen):
            expr = self.expr()
            self.consume(TType.RightParen, "Expected ')' after grouping")
            return Expr.Grouping(expr)

        if self.match(TType.LeftBrace):
            stmts = self.block()
            return Expr.BlockExpr(stmts)

        tok = self.peek()
        raise EoSyntaxError(tok.lf, f"Unexpected token '{tok.ttype}'")

    """ Utils """

    def get(self, *ttypes: TType):
        for ttype in ttypes:
            if self.check(ttype):
                self.next()
                return True

        return False

    def match(self, *types: TType):
        """if it matches, consume it, otherwise do nothing"""
        for type in types:
            if self.check(type):
                self.next()
                return True

        return False

    def check(self, type: TType):
        """Check if the current (unconsumed) token is the ttype we want"""
        if self.is_end():
            return False
        return self.peek().ttype == type

    def consume(self, token: TType, msg: str):
        if self.check(token):
            return self.next()

        # no sync-ing can be done
        # a raise terminates the whole process straight to catch
        raise EoSyntaxError(self.peek().lf, msg)

    """ Pos """

    def is_end(self):
        return self.peek().ttype == TType.EOF

    def peek(self, n=0):
        return self.tokens[self.i + n]

    def prev(self):
        return self.tokens[self.i - 1]

    def next(self):
        if not self.is_end():
            self.i += 1
        return self.prev()
