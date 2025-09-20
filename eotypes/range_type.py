from error.error import EoTypeErrorResult, EoPropErrorResult
from .type import Bool, Type
from .num import Num


class Range(Type):
    start: int
    end: int
    inclusive: bool

    # TODO: what is this
    len: int

    def __init__(self, start: int, end: int, inclusive: bool):
        # todo: make it actually int
        super().__init__(None, "range")
        self.start = start
        self.end = end
        self.inclusive = inclusive

        self.len = max(self.end - self.start, 0)
        if inclusive:
            self.len += 1

    def less(self, right: "Type"):
        if isinstance(right, Range):
            return Bool(self.len < right.len)

        raise EoTypeErrorResult(self, right)

    def grtr(self, right: "Type"):
        if isinstance(right, Range):
            return Bool(self.len < right.len)

        raise EoTypeErrorResult(self, right)

    def prop(self, name: str) -> "Type":
        # TODO: make this efficient
        if name == "len":
            return Num(self.len)
        raise EoPropErrorResult(name, self.tname)

    def to_string(self):
        return f"{self.start}..{'=' if self.inclusive else ''}{self.end}"
