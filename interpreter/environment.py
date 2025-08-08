from eotypes import Type
from error import EoRuntimeError
from tokens import Token


class Environment:
    def __init__(self, parent: "Environment | None" = None) -> None:
        """
        We use a 'parent-pointer tree' here because every part of the stack needs to be preserved
        If there were only braces in the language, sure. The whole runtime would look like a stack.
        But, it's not. We add closures. It's no longer like a stack. Take this example:
        ```
        use io.println;

        fn make_counter() {
            var count = 0;
            fn inc() {
                count += 1;
            }
            return inc;
        }

        var c = make_counter();
        c();
        ```
        If envs were a stack, calling `make_counter` would do this:
            1. Add a stack that stores `count` and `inc`.
            2. Pop the stack (remove both vars)

        The resolver doesn't see that, so it will still try to access inc, which no longer exists.
        """
        self.parent = parent
        self.values: dict[str, Type] = {}

    def define(self, name: str, value: Type):
        self.values[name] = value

    def get_at(self, token: Token, scope: int) -> Type:
        name = token.data
        return self.ancestor(scope).values[name]

    def get(self, token: Token) -> Type:
        name = token.data
        if name in self.values:
            return self.values[name]

        assert not self.parent
        # if self.parent:
        #     return self.parent.get(token)

        raise EoRuntimeError(token.lf, f"Undefined variable '{name}'.")

    def assign_at(self, token: Token, value: Type, scope: int):
        name = token.data
        self.ancestor(scope).values[name] = value

    def assign(self, token: Token, value: Type):
        name = token.data
        if name in self.values:
            self.values[name] = value
            return

        assert not self.parent
        # if self.parent:
        #     return self.parent.assign(token, value)

        raise EoRuntimeError(token.lf, f"Undefined variable '{name}'.")

    def ancestor(self, scope: int) -> "Environment":
        env = self
        for _ in range(scope):
            assert env.parent
            env = env.parent
        return env
