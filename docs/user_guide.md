---
icon: material/book-open-page-variant
---

# User Guide

## Supported Types

There is several types builtin language.

| Type              | Values                 |
| ----------------- | ---------------------- |
| `#!dbuf Bool`     | same as bool in Rust   |
| `#!dbuf Int`      | same as i64 in Rust    |
| `#!dbuf Unsigned` | same as u64 in Rust    |
| `#!dbuf Float`    | same as f64 in Rust    |
| `#!dbuf String`   | same as String in Rust |

### Standard Library

!!! danger
    Not implemented

Also there is should(?) be standard library with types.

#### Nat

A type that represents as `#!dbuf Unsigned` and can be matched via
`#!dbuf Suc{prev: Nat}` and `#!dbuf Zero{}`.

#### Timestamp

A type that represents point in time.

## Math operations

Protocol supports standard math operations (+, -, *, /) for numeric types
(`#!dbuf Int`, `#!dbuf Unsigned`) and boolean operations (&, |, !) for `#!dbuf Bool`
type. They can be used to fullfil dependencies in such way.

```dbuf
message IDepended (x Int) {
}

message Example {
    a Int;
    b Int;
    d IDepended (a + b);
}
```

!!! Note
    Math operations errors and overflows should be reported no later that the
    moment object is constructed. So when the object is received it is
    guaranteed that all dependencies can be calculated correctly.

!!! Note
    Math operations are not supported for `#!dbuf Float` since result may
    dramatically vary in different languages.

## Modular System

!!! danger
    Not implemented

Modular system can be implemented in such way.

```dbuf title="person.dbuf"
message Person {
    name String;
    age Int;
}
```

```dbuf title="request1.dbuf"
use "person.dbuf";

message Request {
    person Person.Person;
}
```

```dbuf title="request2.dbuf"
use "person.dbuf" as P;

message Request {
    person P.Person;
}
```

```dbuf title="request3.dbuf"
use "person.dbuf" as */* (1)! */;

message Request {
    person Person;
}
```

1. Raises errors on name collision.

```dbuf title="use_stdlib.dbuf"
use "stdlib/nat.dbuf";

enum List (length Stdlib.Nat.Nat) {
    Zero{} => {
        Nil {}
    }
    Succ{prev: p} => {
        Cons {
            value Int;
            tail List p;
        }
    }
}
```

```dbuf title="convenient_stdlib.dbuf"
use "stdlib/nat.dbuf" as *;

enum List (length Nat) {
    Zero{} => {
        Nil {}
    }
    Succ{prev: p} => {
        Cons {
            value Int;
            tail List p;
        }
    }
}
```

## Comment

!!! danger
    Not implemented

Comments can be single line and multi line.

=== "single line comments"
    ```dbuf
    // just a comment
    // comment to message Example
    message Example (a Int) {
        // comment to field f
        f Int;
        // comment to field g
        g Int;
    }
    ```
=== "multi line comments"
    ```dbuf
    /*
        Multi line comment
        for message Example.
    */
    message Example (a Int) {
        /*
            Multi line comment
            for field f.
        */
        f Int;
        /*
            Multi line comment
            for field g.
        */
        g Int;
    }
    ```

Although comments can be placed in other places such in next example, it is not
recommended since formatter can simply erase them.

```dbuf
// comment

message Example (a /* comment */ Int) { // comment
    f Int; // Not a comment to field f
    g Int;
    // comment
}
```

More can be find in [parsing section](parsing/#comment-parsing).

## Supported Languages

DependoBuf support quite limited number of languages right now.
If your language is not in supported list, then you can open issue
and eventually language might be supported.

### Kotlin

!!! info
    Documentation is not ready. Here should be hello world example
    to pass message in Kotlin using DBuf.

### Rust

!!! info
    Documentation is not ready. Here should be hello world example
    to pass message in Rust using DBuf.

### Swift

!!! info
    Documentation is not ready. Here should be hello world example
    to pass message in Swift using DBuf.
