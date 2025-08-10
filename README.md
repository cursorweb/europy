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
    ```eo
    fn add(a, b, c = 5) {
        return a + b + c;
    }
    add(1, 2, 3);
    ```
    No longer *need* to name optional arguments (e.g. `c = 3`). You can, however, they must come after unnamed (positional) arguments. Function binding is now very similar to python's strategy.
    
    Also, you can't have duplicate parameters. This no longer works:
    ```
    fn dup(a, a) {}
    ```
* Function printing
    ```eo
    use io.println;
    println(println); // <builtin fn> instead of <Native Fn>
    fn a() {}
    println(a); // <fn a> instead of <User Fn a>
    ```
* Strings. They now compare by length (although in the future, this may be alphanumerically, like 'a' < 'b')
* Expressions. Everything is an expression now. So, these examples are possible:
    ```eo
    use io.println;

    fn factorial(number) {
        if n < 1 {
            1
        } else {
            n * factorial(n - 1)
        }
    }

    var sum_of_five = { // todo: add for loops and make this better!
        var i = 0, sum = 0;
        while i <= 5 {
            sum += i;
            i += 1
        }
        sum
    };

    println(sum_of_five)
    ```
    The rules are simple: you can omit a semicolon if it is there is a right brace or it is the end of file.
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