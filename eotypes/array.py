from error.error import EoTypeErrorResult, EoIndexErrorResult
from .type import Bool, Type
from .num import Num


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

    def get(self, index: "Type") -> "Type":
        idx = self.validate_index(index)
        return self.val[idx]

    def set(self, index: "Type", val: "Type"):
        idx = self.validate_index(index)
        self.val[idx] = val

    def validate_index(self, i: "Type"):
        if not isinstance(i, Num):
            raise EoTypeErrorResult(i)

        idx = i.val

        if int(idx) != idx:
            raise EoIndexErrorResult(i, f"Index must be an integer")

        if idx < 0 or idx >= len(self.val):
            raise EoIndexErrorResult(
                i, f"Out of bounds (index {i}) for length {len(self.val)}"
            )

        return int(idx)
