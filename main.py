from debug import Printer
from lexer import Lexer
from parser import Parser
from interpreter import Interpreter
from parser.nodes import *  # hack

from sys import exit

from error import EoError
from parser.resolver import Resolver

FILENAME = "./test/playground.eo"

lexer = Lexer.from_file(FILENAME)
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
    pass
    print(Printer(tree).run())

resolver = Resolver(trees)
errs = resolver.run()
if len(errs):
    for err in errs:
        err.display()
    exit()

interpreter = Interpreter(trees, FILENAME)

try:
    # dbg:
    # print(interpreter.eval_expr(trees[0].expr).to_string())  # type: ignore
    #:dbg
    interpreter.run()
except EoError as e:
    e.display()
    exit()

# print(res.to_string())
