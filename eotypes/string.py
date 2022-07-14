from tokens import TType, Token
from .type import Type

class String(Type):
    def __init__(self, val: str):
        super().__init__(val, 'string')
    
    def binary(self, op: Token, right: 'Type') -> 'Type':
        if op.ttype == TType.Plus:
            if right.tname == 'string':
                return String(self.val + right.val)
            elif right.tname == 'num':
                return String(self.val + right.to_string())

        return super().binary(op, right)
    
    def to_string(self):
        v = self.val.replace('"', '\\"')
        return f'"{v}"'