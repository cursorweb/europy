from abc import ABC, abstractmethod


# interpreter will extend both
class StmtVisitor(ABC):
    @abstractmethod
    def expr_stmt(self, e):
        pass

    @abstractmethod
    def var_decl(self, e):
        pass

    @abstractmethod
    def block_stmt(self, e):
        pass

    @abstractmethod
    def if_stmt(self, e):
        pass

    @abstractmethod
    def while_stmt(self, e):
        pass

    @abstractmethod
    # break and continue
    def loop_flow(self, e):
        pass

    @abstractmethod
    def ret_stmt(self, e):
        pass

    @abstractmethod
    def function(self, e):
        pass

    @abstractmethod
    def use_stmt(self, e):
        pass


class Stmt(ABC):
    @abstractmethod
    def visit(self, v: StmtVisitor):
        pass
