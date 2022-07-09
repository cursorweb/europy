from tokenize import Token
from typing import Any
from error.error import EoTypeError
from tokens import Token


class Type:
    tname: str
    """ Type Name """

    def __init__(self, val: Any):
        self.val = val # actual value repr
    
    def to_string(self):
        return str(self.val)
    
    def binary(self, op: Token, right: 'Type'):
        raise EoTypeError(op, f"Can't add type {self.tname} with type {right.tname}")
    
    def unary(self, op: Token):
        raise EoTypeError(op, f"Operator '{op.ttype}' can't be applied to type {self.tname}")