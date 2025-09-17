from error.error import EoTypeErrorResult, EoIndexErrorResult
from .type import Bool, Type
from .num import Num


class Map(Type):
    val: dict[Type, Type]

    def __init__(self, val: list[Type]):
        super().__init__(val, "map")

    def less(self, right: "Type"):
        if right.tname == "map":
            return Bool(len(self.val) < len(right.val))

        raise EoTypeErrorResult(self, right)

    def grtr(self, right: "Type"):
        if right.tname == "map":
            return Bool(len(self.val) > len(right.val))

        raise EoTypeErrorResult(self, right)

    def get(self, index: "Type") -> "Type":
        idx = self.validate_index(index)
        return self.val[idx]

    def set(self, index: "Type", val: "Type"):
        idx = self.validate_index(index)
        self.val[idx] = val

    def validate_index(self, idx: "Type"):
        if not idx in self.val:
            raise EoIndexErrorResult(idx, f"{idx} does not exist")

        return idx
