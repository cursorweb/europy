# Europy
What would happen if Europa lang was finished?

This is **NOT** a replacement for Europa, nor is it a rewrite. This is just for entertainment purposes only.

## Motivation
Europa lang, as some of you may know, is plagued with a scope bug that I have no idea how to fix. I don't know where the origin is from, nor do I know what's causing it. To this end, europa lang development has stagnated for a very long time. I finally decided to try something new related to europa lang when the computer I used to dev europa had its display broken, causing an indefinite delay (as if it wasn't already) to development.

This (hopefully) doesn't mean europa lang in rust no longer gets development, I would very much like to see it compiled in wasm (somehow?) and run in the browser among other things, but think of it as a little side project while we wait.

Addendum: Through the rewrite, I'm able to further examine the code and re-organize the project to be easier to work on as well.

## File Structure
- `eotypes` - The native types of europy, bools, nums, etc
- `error` - The thrown errors, like syntaxerror etc, also includes lineinfo (lf)
- `idea` - grammar.txt
- `parser`
    - `nodes`: representation of the tree, binary expr, if stmts etc
    - `parser.py`: actual parsing

- `test`
    - Remember `playground.eo`?

- `lexer.py`:
    - creates tokens from the file

- `tokens.py`:
    - TType, Token

- `interpreter.py`:
    - executes the code