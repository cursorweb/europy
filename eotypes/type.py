from typing import Any
from error.error import EoTypeErrorResult
from abc import ABC


class Type(ABC):
    tname: str
    """ Type Name """

    def __init__(self, val: Any, tname: str):
        self.val = val  # actual value repr
        self.tname = tname

    def to_string(self):
        return str(self.val)

    def plus(self, right: "Type") -> "Type":
        raise EoTypeErrorResult(self, right)

    def minus(self, right: "Type") -> "Type":
        raise EoTypeErrorResult(self, right)

    def times(self, right: "Type") -> "Type":
        raise EoTypeErrorResult(self, right)

    def divide(self, right: "Type") -> "Type":
        raise EoTypeErrorResult(self, right)

    def mod(self, right: "Type") -> "Type":
        raise EoTypeErrorResult(self, right)

    def pow(self, right: "Type") -> "Type":
        raise EoTypeErrorResult(self, right)

    def equals(self, right: "Type") -> "Type":
        return Bool(self.tname == right.tname and self.val == right.val)

    def nequals(self, right: "Type") -> "Type":
        return Bool(self.tname != right.tname and self.val != right.val)

    def grtr(self, right: "Type") -> "Type":
        raise EoTypeErrorResult(self, right)

    def less(self, right: "Type") -> "Type":
        raise EoTypeErrorResult(self, right)

    def grtre(self, right: "Type") -> "Type":
        return Bool(not self.less(right).val)

    def lesse(self, right: "Type") -> "Type":
        return Bool(not self.grtr(right).val)

    def negate(self) -> "Type":
        raise EoTypeErrorResult(self)

    def not_op(self) -> "Type":
        raise EoTypeErrorResult(self)

    def __repr__(self) -> str:
        return self.to_string()


class Bool(Type):
    val: bool

    def __init__(self, val: bool):
        super().__init__(val, "bool")

    def not_op(self) -> "Type":
        return Bool(not self.val)

    def to_string(self):
        return "true" if self.val else "false"
