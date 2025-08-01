# Europy
What would happen if Europa lang was finished?

This is **NOT** a replacement for Europa, nor is it a rewrite. This is just for entertainment purposes only.

## Updates
* New while loop construct:
    ```eo
    while {
        // runs forever
    }
    ```
* Function rework
    ```
    fn add(a, b, c = 5) {
        return a + b + c;
    }
    add(1, 2, 3);
    ```
    No longer *need* to name optional arguments (e.g. `c = 3`). You can, however, they must come after unnamed arguments.
    **todo**: decide what to do with duplicate params (e.g. `fn add(b, b)`)
* Module strategy: imported modules need to have a `mod` statement (or something similar) as the first statement, and they may not run code. Then, whenever a file is referenced, load it in. And then execute the main file.

## Motivation
i have new ideas for europa, after being on hiatus, and i feel like to iterate faster, i should use python.

---
**old motivation:**
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