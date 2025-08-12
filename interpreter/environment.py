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

        The resolver builds this code:
        ```
        fn make_counter() {
            var count = 0;
            fn inc() {
                count#1 += 1;
            }
            return inc#0;
        }

        var c = make_counter#g();
        ```
        When it calls `make_counter`,
        it's going to pass in a new reference to `inc` that lives in the stack we just popped out (it's deleted).
        So, we need that stack to remain alive for as long as *every scope that uses it remains alive*.
        **Not how long the scope itself lives!** For this reason, we use the parent pointer tree structure.
        Functionally, it acts like a stack, **but** the difference is it doesn't free up stacks until *no one needs it anymore*
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

        # should be global
        assert not self.parent

        raise EoRuntimeError(token.lf, f"Undefined variable '{name}'.")

    def assign_at(self, token: Token, value: Type, scope: int):
        name = token.data
        self.ancestor(scope).values[name] = value

    def assign(self, token: Token, value: Type):
        name = token.data
        if name in self.values:
            self.values[name] = value
            return

        # should be global
        assert not self.parent

        raise EoRuntimeError(token.lf, f"Undefined variable '{name}'.")

    def ancestor(self, scope: int) -> "Environment":
        env = self
        for _ in range(scope):
            assert env.parent
            env = env.parent
        return env
