from lexer import Lexer
from parser import Parser
from interpreter import Interpreter
from tokens import TType

from error.lf import LineInfo
from error import EoError

lexer = Lexer.from_repl('''
+ * **
/* a b c
*/
// ee
-
''')

try:
    for token in lexer.run():
        print(token.ttype, token.lf.line, token.lf.col)
except EoError as e:
    e.display()