from abc import ABC, abstractmethod
from collections.abc import Callable as PyFn
from typing import TYPE_CHECKING

from eotypes.nil import Nil
from error.error import EoRuntimeError, FnReturn
from interpreter.environment import Environment
from parser.nodes.stmt.base import Stmt
from tokens import Token
from .type import Type

if TYPE_CHECKING:
    from interpreter.interpreter import Interpreter


class Callable(Type, ABC):
    def __init__(self, params: list[str], opt_params: list[tuple[str, Type]]):
        """
        strategy: fill up as many args as possible,
        then fill up opt_args.
        Finally, used named variables to assign guys by creating a map str -> index

        Also, use the method: len(min_arity) <= len(args) <= len(max_arity) to determine correctness
        """
        """
        Guys:
        ```
        use io.println;
        fn square(n) { return n ** 2; }
        (println + square)(5) // equivalent to println(square(5))
        ```
        """
        self.min_arity = len(params)
        self.max_arity = len(params) + len(opt_params)
        self.tname = "function"

        self.params = params
        self.opt_params = opt_params
        self.param_names = set(params) | set(name for name, _ in opt_params)

    def call(
        self, paren: Token, pos_args: list[Type], named_args: dict[str, Type]
    ) -> Type:
        bound_args = self.bind(paren, pos_args, named_args)
        return self.exec(bound_args)

    def bind(
        self, paren: Token, pos_args: list[Type], named_args: dict[str, Type]
    ) -> dict[str, Type]:
        """
        Bind the arguments to the call, and then `exec` the call

        Let pos_arity = len(params), total_arity = len(params) + len(opt_params)
        1. Check correct arity
        2. Assign all positional arguments (x > pos_arity is an opt_param) to the bound dict
        3. Assign all named arguments by setting the map. Check to make sure that no argument is *re-assigned*
        4. Assign default values to any remaining args that don't exist on bound_args
        5. Check to make sure that no positional args are missing
        6. Check to make sure that there are no extraneous arguments
        """
        # check correct arity:
        total_args = len(pos_args) + len(named_args)
        if not (self.min_arity <= total_args <= self.max_arity):
            argrange = f"{self.min_arity}{f' to {self.max_arity}' if self.max_arity != self.min_arity else ''}"
            raise EoRuntimeError(
                paren.lf, f"Too many arguments. (Got {total_args}, expected {argrange})"
            )

        bound_args: dict[str, Type] = {}

        params = self.params
        opt_params = self.opt_params
        param_names = self.param_names

        # assign all positional arguments
        for i, value in enumerate(pos_args):
            if i < len(params):
                name = params[i]
                bound_args[name] = value
            else:
                idx = i - len(params)
                assert idx < len(opt_params)
                name, _ = opt_params[idx]
                bound_args[name] = value

        # assign all named args, check no argument is reassigned
        for name, value in named_args.items():
            if not name in bound_args:
                bound_args[name] = value
            else:
                raise EoRuntimeError(paren.lf, f"Duplicate argument '{name}'.")

        # assign all default values that haven't been initialized yet
        for name, value in self.opt_params:
            if not name in bound_args:
                bound_args[name] = value

        # check that no required params are missing:
        for param in self.params:
            if not param in bound_args:
                raise EoRuntimeError(
                    paren.lf, f"Missing argument for parameter '{param}'."
                )

        # check that no extraneous params are present:
        for name in bound_args:
            if name not in param_names:
                raise EoRuntimeError(paren.lf, f"Unexpected named argument '{name}'.")

        return bound_args

    @abstractmethod
    def exec(self, args: dict[str, Type]) -> Type:
        """Actually run code here"""
        pass


def make_fn(
    params: list[str],
    opt_params: list[tuple[str, Type]],
    fn: PyFn[[dict[str, Type]], Type],
):
    class Out(Callable):
        def __init__(self):
            super().__init__(params, opt_params)
            self.val = f"<builtin fn>"

        def exec(self, args: dict[str, Type]) -> Type:
            return fn(args)

    return Out()


class EoFunction(Callable):
    def __init__(
        self,
        name: str,
        params: list[str],
        opt_params: list[tuple[str, Type]],
        block: list[Stmt],
        interpreter: "Interpreter",
    ):
        super().__init__(params, opt_params)
        self.val = f"<fn {name}>"
        self.block = block
        self.interpreter = interpreter
        self.closure = interpreter.env

    def exec(self, args: dict[str, Type]) -> Type:
        interpreter = self.interpreter
        env = Environment(self.closure)
        for arg, val in args.items():
            env.define(arg, val)

        try:
            out = interpreter.eval_block(self.block, env)
        except FnReturn as r:
            out = r.val

        return out
