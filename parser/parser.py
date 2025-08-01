from typing import NoReturn

import eotypes
from error.error import EoSyntaxError

from parser.nodes.expr.base import Expr as ExprT
import parser.nodes.expr.node as Expr

from parser.nodes.stmt.base import Stmt as StmtT
import parser.nodes.stmt.node as Stmt

from tokens import TType, Token


class Parser:
    # todo: add sync
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.i = 0

    def run(self) -> tuple[list[EoSyntaxError], list[StmtT]]:
        stmts = []
        errors = []

        while not self.is_end():
            try:
                stmts.append(self.stmt())
            except EoSyntaxError as e:
                errors.append(e)

        return errors, stmts

    """ - AST - """
    """ Stmt """

    def stmt(self) -> StmtT:
        if self.match(TType.If):
            return Stmt.IfStmt(*self.if_stmt())

        if self.match(TType.Var):
            return self.var_decl()

        if self.match(TType.Fn):
            return self.fn_decl()

        if self.match(TType.While):
            return self.while_stmt()

        if self.match(TType.Do):
            return self.dowhile_stmt()

        if self.match(TType.For):
            return self.for_stmt()

        if self.match(TType.LeftBrace):
            return Stmt.BlockStmt(self.block())

        if self.match(TType.Break, TType.Continue, TType.Return):
            return self.controlflow_stmt()

        if self.match(TType.Use):
            pass

        return self.expr_stmt()

    def if_stmt(
        self,
    ) -> tuple[ExprT, list[StmtT], list[tuple[ExprT, list[StmtT]]], list[StmtT] | None]:
        cond = self.expr()
        self.consume(TType.LeftBrace, "Expected '{' after if statement condition.")
        true_br = self.block()
        elif_brs: list[tuple[ExprT, list[StmtT]]] = []
        else_br = None

        while self.match(TType.Elif):
            elif_cond = self.expr()
            self.consume(
                TType.LeftBrace, "Expected '{' after elif statement condition."
            )
            elif_brs.append((elif_cond, self.block()))

        if self.match(TType.Else):
            self.consume(TType.LeftBrace, "Expected '{' after else keyword.")
            else_br = self.block()

        return (cond, true_br, elif_brs, else_br)

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
                    self.report_err(
                        self.prev(),
                        "Expected ',' or ';' after variable declaration.",
                    )
            else:
                self.report_err(self.prev(), "Expected variable name.")

        return Stmt.VarDecl(vars)

    def fn_decl(self) -> StmtT:
        name = self.consume(TType.Identifier, "Expected function name")
        self.consume(TType.LeftParen, "Expected '(' after function name")

        params: list[str] = []
        opt_params: list[tuple[str, ExprT]] = []
        seen_opt_params = False

        while not self.check(TType.RightParen):
            param = self.consume(TType.Identifier, "Expected parameter name")

            if not seen_opt_params and self.check(TType.Eq):
                seen_opt_params = True

            if seen_opt_params:
                self.consume(
                    TType.Eq,
                    "Optional parameters may only come after required parameters",
                )
                expr = self.expr()
                opt_params.append((param.data, expr))
            else:
                params.append(param.data)

            if not self.match(TType.Comma):
                break

        self.consume(TType.RightParen, "Expected ')' after function parameters")
        self.consume(TType.LeftBrace, "Expected '{' after function declaration")
        stmts = self.block()

        return Stmt.Function(name, params, opt_params, stmts)

    def while_stmt(self) -> StmtT:
        cond: ExprT
        if self.match(TType.LeftBrace):
            cond = Expr.LiteralVal(eotypes.Bool(True))
            body = self.block()
        else:
            cond = self.expr()
            self.consume(TType.LeftBrace, "Expected '{' after while loop condition.")
            body = self.block()

        return Stmt.WhileStmt(cond, body)

    def dowhile_stmt(self) -> StmtT:
        tok = self.consume(TType.LeftBrace, "Expected '{' after do keyword.")
        body = self.block()
        self.consume(TType.While, "Expected 'while' after do loop body.")
        cond = self.expr()
        self.consume(TType.Semi, "Expected ';' after do while loop condition.")

        return Stmt.WhileStmt(
            Expr.LiteralVal(eotypes.Bool(True)),
            [*body, Stmt.IfStmt(cond, [Stmt.LoopFlow(tok, "break")], [])],
        )

    def for_stmt(self) -> StmtT:
        ident = self.consume(TType.Identifier, "Expected variable after 'for'.")
        self.consume(TType.In, "Expected 'in' after variable name")
        iterator = self.expr()
        block = self.block()

        return Stmt.ForStmt(ident.data, iterator, block)

    def block(self) -> list[StmtT]:
        """Make sure to consume '{'"""
        stmts = []

        while not self.check(TType.RightBrace) and not self.is_end():
            stmts.append(self.stmt())

        self.consume(TType.RightBrace, "Expected '}' after block expression.")

        return stmts

    def controlflow_stmt(self) -> StmtT:
        tok = self.prev()
        stmt: StmtT

        if tok.ttype == TType.Break:
            stmt = Stmt.LoopFlow(tok, "break")
        elif tok.ttype == TType.Continue:
            stmt = Stmt.LoopFlow(tok, "continue")
        elif tok.ttype == TType.Return:
            val = None
            if not self.get(TType.Semi):
                val = self.expr()
            stmt = Stmt.RetStmt(tok, val)
        else:
            raise Exception("unreachable")

        self.consume(TType.Semi, "Expected ';' after control flow")
        return stmt

    def expr_stmt(self) -> StmtT:
        expr = self.expr()

        if not self.match(TType.Semi):
            semi = self.peek()
            # feature: last statement doesn't need semi (repl purposes probably)
            if semi.ttype != TType.RightBrace and semi.ttype != TType.EOF:
                self.report_err(semi, "Expected ';' after statement.")

        return Stmt.ExprStmt(expr)

    """ Expr """

    def expr(self) -> ExprT:
        return self.ternary()

    def ternary(self) -> ExprT:
        expr = self.assignment()

        if self.match(TType.Question):
            if_true = self.expr()
            self.consume(TType.Colon, "Expected ':' after ternary if then expression")
            els = self.ternary()

            expr = Expr.IfExpr(expr, [Stmt.ExprStmt(if_true)], [], [Stmt.ExprStmt(els)])

        return expr

    def assignment(self) -> ExprT:
        expr = self.logic_or()
        if self.match(
            TType.Eq,
            TType.PlusEq,
            TType.MinusEq,
            TType.TimesEq,
            TType.DivideEq,
            TType.PowEq,
            TType.ModEq,
        ):
            if not isinstance(expr, Expr.Variable):
                self.report_err(self.prev(), "Invalid assignment target")
            name = expr.name
            assign_op = self.prev()
            val = self.expr()
            if assign_op.ttype == TType.Eq:
                expr = Expr.Assign(name, val)
            else:
                match assign_op.ttype:
                    case TType.PlusEq:
                        op = TType.Plus
                    case TType.MinusEq:
                        op = TType.Minus
                    case TType.TimesEq:
                        op = TType.Times
                    case TType.DivideEq:
                        op = TType.Divide
                    case TType.PowEq:
                        op = TType.Pow
                    case TType.ModEq:
                        op = TType.Mod

                expr = Expr.Assign(
                    name,
                    Expr.Binary(Expr.Variable(name), Token(op, assign_op.lf), val),
                )
        return expr

    def logic_or(self) -> ExprT:
        expr = self.logic_and()
        while self.match(TType.Or):
            tok = self.prev()
            right = self.logic_and()
            expr = Expr.Logical(expr, tok, right)

        return expr

    def logic_and(self) -> ExprT:
        expr = self.equality()
        while self.match(TType.And):
            tok = self.prev()
            right = self.equality()
            expr = Expr.Logical(expr, tok, right)

        return expr

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

        return self.call()

    def call(self) -> ExprT:
        expr = self.primary()

        if self.match(TType.LeftParen):
            paren = self.prev()
            args: list[ExprT] = []
            named_args: list[tuple[Token, ExprT]] = []
            seen_named_args = False

            while not self.check(TType.RightParen):
                if (
                    not seen_named_args
                    and self.check(TType.Identifier)
                    and self.check(TType.Eq, 1)
                ):
                    seen_named_args = True

                if seen_named_args:
                    name = self.consume(
                        TType.Identifier,
                        "Named arguments may only come after positional arguments",
                    )
                    self.consume(
                        TType.Eq,
                        "Expected '=' after argument name",
                    )
                    val = self.expr()
                    named_args.append((name, val))
                else:
                    args.append(self.expr())

                if not self.match(TType.Comma):
                    break

            self.consume(TType.RightParen, "Expected ')' after arguments.")
            expr = Expr.Call(expr, paren, args, named_args)
        return expr

    def primary(self) -> ExprT:
        if self.match(TType.T_True):
            return Expr.LiteralVal(eotypes.Bool(True))
        if self.match(TType.T_False):
            return Expr.LiteralVal(eotypes.Bool(False))
        if self.match(TType.Nil):
            return Expr.LiteralVal(eotypes.Nil())

        if self.match(TType.If):
            return Expr.IfExpr(*self.if_stmt())

        if self.match(TType.Number, TType.String):
            t = self.prev()
            if t.ttype == TType.String:
                return Expr.LiteralVal(eotypes.String(t.data))
            else:
                return Expr.LiteralVal(eotypes.Num(t.data))

        if self.match(TType.Identifier):
            name = self.prev()
            return Expr.Variable(name)

        if self.match(TType.LeftParen):
            expr = self.expr()
            self.consume(TType.RightParen, "Expected ')' after grouping")
            return Expr.Grouping(expr)

        if self.match(TType.LeftBrace):
            stmts = self.block()
            return Expr.BlockExpr(stmts)

        tok = self.peek()
        self.report_err(tok, f"Unexpected token '{tok.ttype}'")

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

    def check(self, type: TType, n=0):
        """Check if the current (unconsumed) token is the ttype we want"""
        if self.is_end():
            return False
        return self.peek(n).ttype == type

    def consume(self, token: TType, msg: str):
        if self.check(token):
            return self.next()

        self.report_err(self.peek(), msg)

    def report_err(self, tok: Token, msg: str) -> NoReturn:
        err = EoSyntaxError(tok.lf, msg)
        self.synchronize()
        raise err

    def synchronize(self):
        while not self.is_end():
            if self.prev().ttype == TType.Semi:
                # we want to make sure the semicolon is consumed
                return

            # these guys match the start of a statement probably
            # so don't eat them!
            match self.peek().ttype:
                case (
                    TType.Use
                    | TType.Fn
                    | TType.For
                    | TType.If
                    | TType.Return
                    | TType.While
                ):
                    return

            self.next()

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
