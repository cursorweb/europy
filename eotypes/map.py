from error.error import EoTypeErrorResult, EoIndexErrorResult
from .type import Bool, Type
from .num import Num


class Map(Type):
    val: dict[Type, Type]

    def __init__(self, val: dict[Type, Type]):
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
        # todo: actually have a hash
        self.val[index.val] = val

    def validate_index(self, idx: "Type"):
        i = idx.val
        if not i in self.val:
            raise EoIndexErrorResult(idx, f"{idx} does not exist")

        return i

    def to_string(self):
        values = ", ".join([f"{k}: {v}" for k, v in self.val.items()])
        return f"{{{{ {values} }}}}"
