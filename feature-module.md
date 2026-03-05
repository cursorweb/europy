# Modules V1

```
// math.eo
var PI = 3.14;

fn add(a, b) {
    a + b
}

fn multiply(a, b) {
    a * b
}
```

## Namespace import
Simply brings all the variables into a "namespace"
```
// main.eo
use math;
use io.println;

println(math.PI);
math.add(3, 4);
```

## Folder import
Use `folder.file` syntax to import a nested file. You can't really import parent files.
```
/*
main.eo
utils/
    string.eo
    math/
        trig.eo
*/

// main.eo
use utils.math.trig;
trig.sin();

// utils.eo
use math.trig;
```

## Cyclic Import
You can't have cyclic imports.

## Execution
The entire file executes **once** on the first `use`. And not again.