from .type import Type
from enum import Enum
from ..interpreter.environment import Environment


class ModuleState(Enum):
    NotLoaded = 0
    Loading = 1
    Loaded = 2


class Module(Type):
    val: Environment

    def __init__(self, val: Environment):
        super().__init__(val, "module")
        self.status = ModuleState.NotLoaded

    def prop(self, name: str) -> "Type":
        value = self.val.get_str(name)
        if value is None:
            raise RuntimeError(f"Module has no property '{name}'")
        return value
