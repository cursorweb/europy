from abc import ABC, abstractmethod

from tokens import Token


# interpreter will extend both
class StmtVisitor(ABC):
    pass # todo!

class Stmt(ABC):
    @abstractmethod
    def visit(self, v: StmtVisitor): pass