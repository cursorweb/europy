from typing import Any
from error.error import EoTypeError
from tokens import Token
from abc import ABC


class Type(ABC):
    tname: str
    """ Type Name """

    def __init__(self, val: Any, tname: str):
        self.val = val  # actual value repr
        self.tname = tname

    def to_string(self):
        return str(self.val)

    def binary(self, op: Token, right: "Type") -> "Type":
        raise EoTypeError(
            op,
            f"Operator '{op.ttype}' can't be used with type {self.tname} and {right.tname}",
        )

    def unary(self, op: Token) -> "Type":
        raise EoTypeError(
            op, f"Operator '{op.ttype}' can't be applied to type {self.tname}"
        )
