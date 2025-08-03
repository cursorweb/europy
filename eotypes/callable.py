from abc import ABC, abstractmethod
from collections.abc import Callable as PyFn

from error.error import EoRuntimeError
from tokens import Token
from .type import Type


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
        self.tname = "<native fn>"

        self.params = params
        self.opt_params = opt_params
        self.param_names = set(params) | set(name for name, _ in opt_params)

    def call(self, paren: Token, pos_args: list[Type], named_args: dict[str, Type]):
        bound_args = self.bind(paren, pos_args, named_args)
        self.exec(bound_args)

    def bind(
        self, paren: Token, pos_args: list[Type], named_args: dict[str, Type]
    ) -> dict[str, Type]:
        """
        Bind the arguments to the call, and then `exec` the call

        Let pos_arity = len(params), total_arity = len(params) + len(opt_params)
        1. Check correct arity
        2. Initialize bound_args with default values
        3. Assign all positional arguments (x > pos_arity is an opt_param) to the bound dict
        4. Assign all named arguments by setting the map. Check to make sure that no argument is *re-assigned*
        5. Check to make sure that there are no extraneous arguments
        """
        # check correct arity:
        total_args = len(pos_args) + len(named_args)
        if not (self.min_arity <= total_args <= self.max_arity):
            argrange = f"{self.min_arity}{f' to {self.max_arity}' if self.max_arity != self.min_arity else ''}"
            raise EoRuntimeError(
                paren.lf, f"Too many arguments. (Got {total_args}, expected {argrange})"
            )

        bound_args: dict[str, Type] = {}

        for name, value in self.opt_params:
            bound_args[name] = value

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

        # assign all named args
        for name, value in named_args.items():
            if not name in bound_args:
                bound_args[name] = value
            else:
                raise EoRuntimeError(paren.lf, f"Duplicate argument '{name}'.")

        for param in self.params:
            # check that no required params are missing:
            if not param in bound_args:
                raise EoRuntimeError(
                    paren.lf, f"Missing argument for parameter '{param}'."
                )

        # check that no extraneous params are present:
        for name in bound_args:
            if name not in param_names:
                raise EoRuntimeError(paren.lf, f"Unexpected named argument '{param}'.")

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

        def exec(self, args: dict[str, Type]) -> Type:
            return fn(args)

    return Out()
