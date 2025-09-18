from error.error import EoTypeErrorResult, EoIndexErrorResult
from .type import Bool, Type
from .num import Num

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from parser.nodes.expr.node import MapExpr


class Map(Type):
    val: dict[str, Type]

    def __init__(self, val: dict[str, Type]):
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
        self.val[self.key(index)] = val

    @classmethod
    def key(cls, k: "Type"):
        return f"{k.tname}!{k!r}"

    def validate_index(self, idx: "Type"):
        i = self.key(idx)
        if not i in self.val:
            raise EoIndexErrorResult(idx, f"{idx} does not exist")

        return i

    def to_string(self):
        values = ", ".join([f"{k.split('!', 1)[1]}: {v}" for k, v in self.val.items()])
        return f"{{{{ {values} }}}}"
