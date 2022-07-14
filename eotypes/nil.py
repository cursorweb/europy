from .type import Type

class Nil(Type):
    def __init__(self):
        super().__init__(None, 'nil')
    
    def to_string(self):
        return 'nil'