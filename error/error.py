from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from tokens import Token
    from eotypes import Type
from .lf import LineInfo


class EoError(BaseException):
    def __init__(self, etype: str, lf: "LineInfo", msg: str):
        """
        etype: The error type, e.g. SyntaxError
        lf: LineInfo, e.g. line 1 col 1
        msg: The error message, e.g. unexpected token class ;)
        """
        self.etype = etype
        self.lf = lf
        self.msg = msg

    def display(self):
        print(
            f"File '{self.lf.file}' [{self.lf.line}:{self.lf.col}] {self.etype} {self.msg}"
        )


class EoIoError(EoError):
    def __init__(self, file: str, e: BaseException):
        super().__init__(
            "IoError", LineInfo(file, 1, 1), f"Unable to open file {file}. {e}"
        )


class EoSyntaxError(EoError):
    def __init__(self, lf: "LineInfo", msg: str):
        super().__init__("SyntaxError", lf, msg)


class EoRuntimeError(EoError):
    def __init__(self, lf: LineInfo, msg: str):
        super().__init__("RuntimeError", lf, msg)


class EoTypeError(EoError):
    def __init__(self, lf: "LineInfo", msg: str):
        super().__init__("TypeError", lf, msg)


class EoErrorResult(ABC, BaseException):
    """Raise a type error that gets promoted to a EoTypeError (EoErrorResult does not have line info)"""

    @abstractmethod
    def with_lf(self, op: "Token") -> EoError:
        pass


class EoTypeErrorResult(EoErrorResult):
    def __init__(self, *types: "Type"):
        self.types = map(lambda t: t.tname, types)

    def with_lf(self, op: "Token"):
        return EoTypeError(
            op.lf,
            f"Operator '{op.ttype.value}' can't be applied to {', '.join(self.types)}",
        )


class EoIndexErrorResult(EoErrorResult):
    def __init__(self, key: "Type", message: str | None):
        self.key = key
        self.message = message

    def with_lf(self, op: "Token"):
        msg = f": {self.message}" if self.message != None else ""
        return EoTypeError(op.lf, f"Invalid index '{self.key}'{msg}.")


class LoopBreak(BaseException):
    """Make sure to catch this in ALL loops"""

    def __init__(self, val: "Type") -> None:
        self.val = val


class LoopContinue(BaseException):
    pass


class FnReturn(BaseException):
    def __init__(self, val: "Type") -> None:
        self.val = val
