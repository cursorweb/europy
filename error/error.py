from abc import abstractclassmethod

from .lf import LineInfo


class EoError:
    def __init__(self, lf: LineInfo, msg: str):
        self.lf = lf
        self.msg = msg
    
    def display(self):
        print(f"File '{self.lf.file}' [{self.lf.line}:{self.lf.col}] {self.get_error()}")
    
    @abstractclassmethod
    def get_error(self) -> str:
        return self.msg

class SyntaxError(EoError):
    def __init__(self, lf: LineInfo, msg: str):
        super().__init__(lf, msg)
    
    def get_error(self) -> str:
        return f"SyntaxError: {self.msg}"