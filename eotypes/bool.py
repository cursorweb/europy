from tokens import TType, Token
from .type import Type

class Bool(Type):
    def __init__(self, val: bool):
        super().__init__(val, 'bool')
    
    def unary(self, op: Token) -> 'Type':
        if op.ttype == TType.Not:
            return Bool(not self.val)

        return super().unary(op)
    
    def to_string(self):
        return "true" if self.val else "false"