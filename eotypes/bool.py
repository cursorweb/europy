from .type import Type

class Bool(Type):
    def __init__(self, val: bool):
        super().__init__(val)
    
    def to_string(self):
        return "true" if self.val else "false"