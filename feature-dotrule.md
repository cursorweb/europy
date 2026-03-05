# Dot extension
Look at this example:
```
fn (self Number).is_even() {
    return self % 2 == 0;
}

println(5.is_even()); // false
```

Basically, `<expr>.function();` becomes a new operator, and you can define functions on types this way.
The best part about this that it's scoped, so whatever you define on the type, they will disappear after it goes out of scope.
Example usage of this is:
```
use is_even_lib.is_even;

println(4.is_even());
```

Something silly but cool:
```
fn self.print() {
    println(self);
}

[1, 2, 3].print(); // [1, 2, 3]
5.print(); // 5
```