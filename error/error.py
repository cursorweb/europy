from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from tokens import Token
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


class EoTypeError(EoError):
    def __init__(self, lf: "Token", msg: str):
        super().__init__("TypeError", lf.lf, msg)
