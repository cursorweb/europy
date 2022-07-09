from .type import Type

class String(Type):
    def __init__(self, val: str):
        super().__init__(val)
    
    def to_string(self):
        return f'''"{self.val.replace('"', '\\"')}"'''