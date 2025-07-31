from typing import Any
from enum import Enum

from error.lf import LineInfo


class TType(Enum):
    """Delimiters"""

    LeftBBrace = "{{"
    RightBBrace = "}}"

    LeftBrace = "{"
    RightBrace = "}"

    LeftParen = "("
    RightParen = ")"

    LeftBrack = "["
    RightBrack = "]"

    Comma = ","
    Dot = "."

    # ranges
    DotDot = ".."
    DotEq = ".="

    Semi = ";"

    """ Comparison """
    Not = "!"
    EqEq = "=="
    NotEq = "!="
    Greater = ">"
    GreaterEq = ">="
    Less = "<"
    LessEq = "<="

    """ Assignment """
    Eq = "="
    PlusEq = "+="
    MinusEq = "-="
    TimesEq = "*="
    DivideEq = "/="
    PowEq = "**="
    ModEq = "%="

    """ Operators """
    Plus = "+"
    Minus = "-"
    Times = "*"
    Divide = "/"
    Pow = "**"
    Mod = "%"

    Colon = ":"
    Question = "?"

    """ Literals """
    Identifier = "Identifier"
    String = "String"
    Number = "Number"
    T_True = "true"
    T_False = "false"
    Nil = "nil"

    """ Keywords """
    Fn = "fn"
    Return = "return"
    Var = "var"
    Use = "use"
    Do = "do"
    While = "while"
    For = "for"
    In = "in"
    Break = "break"
    Continue = "continue"
    Or = "or"
    And = "and"
    If = "if"
    Else = "else"
    Elif = "elif"

    EOF = "eof"


class Token:
    ttype: TType
    lf: LineInfo
    data: Any

    def __init__(self, ttype: TType, lf: LineInfo, data: Any = None) -> None:
        self.ttype = ttype
        self.lf = lf
        self.data = data

    def __repr__(self) -> str:
        return f"Token('{self.ttype.value}')"
