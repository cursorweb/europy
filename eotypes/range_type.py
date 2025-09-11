from error.error import EoTypeErrorResult
from .type import Bool, Type


class Range(Type):
    start: int
    end: int
    inclusive: bool

    # TODO: what is this
    len: int

    def __init__(self, start: int, end: int, inclusive: bool):
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
