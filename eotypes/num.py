from error.error import EoTypeErrorResult
from .type import Bool, Type
from .string import String


class Num(Type):
    val: float

    def __init__(self, val: float):
        super().__init__(val, "num")

    def to_string(self):
        if self.val.is_integer():
            return str(int(self.val))
        else:
            return str(self.val)

    def plus(self, right: "Type"):
        if right.tname == "num":
            return Num(self.val + right.val)

        if right.tname == "string":
            return String(self.to_string() + right.val)

        raise EoTypeErrorResult(self, right)

    def minus(self, right: "Type"):
        if right.tname == "num":
            return Num(self.val - right.val)

        raise EoTypeErrorResult(self, right)

    def times(self, right: "Type"):
        if right.tname == "num":
            return Num(self.val * right.val)

        raise EoTypeErrorResult(self, right)

    def divide(self, right: "Type"):
        if right.tname == "num":
            return Num(self.val / right.val)

        raise EoTypeErrorResult(self, right)

    def mod(self, right: "Type"):
        if right.tname == "num":
            return Num(self.val % right.val)

        raise EoTypeErrorResult(self, right)

    def pow(self, right: "Type"):
        if right.tname == "num":
            return Num(self.val**right.val)

        raise EoTypeErrorResult(self, right)

    def grtr(self, right: "Type"):
        if right.tname == "num":
            return Bool(self.val > right.val)

        raise EoTypeErrorResult(self, right)

    def less(self, right: "Type"):
        if right.tname == "num":
            return Bool(self.val < right.val)

        raise EoTypeErrorResult(self, right)

    def grtre(self, right: "Type") -> "Type":
        if right.tname == "num":
            return Bool(self.val >= right.val)

        raise EoTypeErrorResult(self, right)

    def lesse(self, right: "Type") -> "Type":
        if right.tname == "num":
            return Bool(self.val <= right.val)

        raise EoTypeErrorResult(self, right)

    def negate(self) -> "Type":
        return Num(-self.val)
