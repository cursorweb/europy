from typing import Literal
from .type import Type


class NativeCallable(Type):
    param_map: dict[str, tuple[Literal["pos"], int] | Literal["opt"]]

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

        # suppose we have function `fn add(a, b, c = 5) {}`
        # then, `param_map = { "a": ('pos', 0), "b": ('pos', 1), "c": 'opt' }`
        # this `param_map` is used for named arguments.
        param_map: dict[str, tuple[Literal["pos"], int] | Literal["opt"]] = {}
        # then, `opt_param_idx = { 2: "c" }`
        # this `opt_param_idx` is used to know where to assign arguments that go above
        # positional argument arity (e.g. c, the '3rd' argument goes *beyond* the expected 2 *positional* arguments, so we need to know which opt_param that is)
        opt_param_idx: dict[int, str] = {}

        for i, param in enumerate(params):
            param_map[param] = ("pos", i)

        arity = self.min_arity
        for i, (param, _) in enumerate(opt_params):
            param_map[param] = "opt"
            opt_param_idx = {arity + i: param}

        self.param_map = param_map
        self.opt_param_idx = opt_param_idx
        self.opt_params = opt_params

    def call(self, pos_args: list[Type], named_args: dict[str, Type]):
        """
        Function to give the correct arguments to the correct people,
        and then call exec which runs the function
        """

        # suppose we have function `fn add(a, b, c = 5) {}` and `add(1, 2, c = 3)`
        # then, `args     = [1, 2]`
        # and,  `opt_args = { "c": 3 }`

        arity = self.min_arity
        args = []
        opt_args = {}
        for i, arg in enumerate(pos_args):
            if i < arity:
                args.append(arg)
            else:
                name = self.opt_param_idx[i]
                opt_args[name] = arg

        for name, val in named_args:
            result = self.param_map[name]
            if result == "opt":
                opt_args[name] = val
            else:
                _, idx = result
                args[idx] = val

    def exec(self, args: list[Type], opt_params: dict[str, Type]):
        """Actually run code here"""
        pass
