from debug import Printer
from lexer import Lexer
from parser import Parser
from interpreter import Interpreter
from parser.nodes import *  # hack

from sys import exit

from error import EoError

lexer = Lexer.from_file("test/playground.eo")

try:
    tokens = lexer.run()
except EoError as e:
    e.display()
    exit()

parser = Parser(tokens)

errs, trees = parser.run()
if len(errs):
    for err in errs:
        err.display()
    exit()

for tree in trees:
    print(Printer(tree).run())


interpreter = Interpreter(trees)

try:
    # dbg:
    # print(interpreter.eval_expr(trees[0].expr).to_string())  # type: ignore
    #:dbg
    interpreter.run()
except EoError as e:
    e.display()
    exit()

# print(res.to_string())
