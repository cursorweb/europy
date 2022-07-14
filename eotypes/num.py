from tokens import TType, Token
from .type import Type

class Num(Type):
    def __init__(self, val: float):
        super().__init__(val, 'num')
    
    def binary(self, op: Token, right: 'Type'):
        if op.ttype == TType.Plus:
            if right.tname == 'num':
                return Num(self.val + right.val)
            elif right.tname == 'string':
                from .string import String
                return String(self.to_string() + right.val)
        
        if op.ttype == TType.Minus and right.tname == 'num':
            return Num(self.val - right.val)
        
        if op.ttype == TType.Times and right.tname == 'num':
            return Num(self.val * right.val)
        
        if op.ttype == TType.Divide and right.tname == 'num':
            return Num(self.val / right.val) # todo: division by 0
        
        if op.ttype == TType.Mod and right.tname == 'num':
            return Num(self.val % right.val)
        
        if op.ttype == TType.Pow and right.tname == 'num':
            return Num(self.val ** right.val)
        
        return super().binary(op, right)
    
    def unary(self, op: Token) -> 'Type':
        if op.ttype == TType.Minus:
            return Num(-self.val)

        return super().unary(op)