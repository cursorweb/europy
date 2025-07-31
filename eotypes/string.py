from error.error import EoTypeErrorResult
from .type import Bool, Type


class String(Type):
    val: str

    def __init__(self, val: str):
        super().__init__(val, "string")

    def plus(self, right: Type):
        if right.tname == "string":
            return String(self.val + right.val)
        return String(self.val + right.to_string())

    def grtr(self, right: "Type"):
        if right.tname == "string":
            return Bool(len(self.val) > len(right.val))

        raise EoTypeErrorResult(self, right)

    def less(self, right: "Type"):
        if right.tname == "string":
            return Bool(len(self.val) < len(right.val))

        raise EoTypeErrorResult(self, right)

    def to_string(self):
        v = self.val.replace('"', '\\"')
        return f'"{v}"'
