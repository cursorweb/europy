from .type import Type

class Num(Type):
    def __init__(self, val: float):
        super().__init__(val)