from error.error import EoTypeErrorResult
from .type import Bool, Type


class Array(Type):
    val: list[Type]

    def __init__(self, val: list[Type]):
        super().__init__(val, "array")

    def less(self, right: "Type"):
        if right.tname == "array":
            return Bool(len(self.val) < len(right.val))

        raise EoTypeErrorResult(self, right)

    def grtr(self, right: "Type"):
        if right.tname == "array":
            return Bool(len(self.val) > len(right.val))

        raise EoTypeErrorResult(self, right)
