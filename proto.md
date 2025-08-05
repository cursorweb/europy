# Prototypes
For object oriented programming, we will have prototypes. Here's a quick example:
```
use io.println;

trait Person {
    name; // these properties need to be defined on the trait
    say_hi(self) {
        println("Hi my name is " + self.name);
    }
}

fn create_person(name) {
    return impl Person for {{ name }};
}

var john = create_person("john");
john.say_hi(); // Hi my name is john.
```
Notice how the trait is separate from the object. Each trait *only* needs to know the bare minimum to implement each interface, letting it be easily re-used on *any* object that has the property.

## Inheritance
Prototypes can then extend prototypes, let's say worker is a subprototype of person, with a property job.
```
trait Work {
    job;
    work(self) {
        println("Working as a " + self.job);
    }
}

fn create_worker(job, name) {
    impl Work, ..create_person(name) for {{ job }};
}

var coder = create_worker("programmer", "frank");
coder.say_hi(); // Hi my name is frank.
coder.work(); // Working as a programmer.
```

> ### Semantic note:
> There's a difference between these two lines:
> ```
> impl NewTrait, ..parent for {{ new_prop }};
> ```
> having `..parent` outside of the object means it inherits both structure *and* traits
> ```
> {{ ..parent, new_prop }}
> ```
> having `..parent` inside the object means it only inherits structure, its methods are not preserved.

## Inline traits
Traits can be inline too, if you just want to quickly add a method to an object:
```
fn create_point(x, y) {
    impl trait {
        debug(self) {
            print(x + ", " + y);
        }
    } for {{ x, y }};
}

create_point(5, 6).debug(); // 5, 6
```

This is useful for debugging, and prototyping. You can later lift traits out of inline mode, to reuse traits.

## Examples
### Square Circle
Suppose you were making a GUI. Then:
```
trait Drawable {
    abstract draw;
}

fn create_square(x, y, w, h) {
    return impl Drawable {
        draw(self) {
            println("Drawing square");
            // do something with x, y, w, h
        }
    } for {{ x, y, w, h }};
}

fn create_circle(x, y, r) {
    return impl Drawable {
        draw(self) {
            println("Drawing circle");
        }
    } for {{ x, y, r }};
}
```
Note the `abstract trait`. Having an abstract trait lets you enforce methods without knowing their implementation. Note abstract methods don't check function signatures, just the presence of the method.

### Hero Enemy
In a game, hero and enemy may share common functionality, such as `is_alive` as well as `move`:
```
trait Mob {
    hp;

    is_alive(self) { self.hp > 0 }
    take_damage(self, dmg) { self.hp -= dmg }

    abstract move;
    abstract attack;
}

fn base_character(hp) {
    return impl Mob for {{ hp }};
}
```