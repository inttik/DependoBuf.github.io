---
icon: material/play-circle-outline 
---

# Get Started

First, [install](install.md) DBuf if haven't done it before.

## Simplest structures

Protocol currently supports creation for only two kinds of object: `#!dbuf message`
and `#!dbuf enum`.

=== "Simple `#!dbuf message`"

    `#!dbuf message` is like improved struct from other languages.

    ```dbuf
    /*
        Multi line comment (1)
    */
    message Person/* (2)! */ {
        age/* (3)! */ Int;
        name String/* (4)! */; // single line comment  (5)
    }
    ```

    1. !!! danger "Currently not supported"
    2. Name of structure
    3. Name of field
    4. Type of field
    5. !!! danger "Currently not supported"

=== "Simple `#!dbuf enum`"

    `#!dbuf enum` is an object that can contain only one of constructors. Also
    in dbuf It allows
    pattern match to has different constructors.

    ```dbuf
    /*
        Multi line comment (1)
    */
    enum Color/* (2)! */ {
        Red/* (3)! */
        Black {}/* (4)! */
        Other/* (5)! */ {
            r/* (6)! */ Int;
            g Int/* (7)! */;
            b Int; // Single line comment (8)
        }
    }
    ```

    1. !!! danger "Currently not supported"
    2. Name of enum
    3. Constructor for enum that has no field
    4. Other way to define empty constructor
    5. Constructor that contains some fields
    6. Name of field of constructor `#!dbuf Other`
    7. Type of field of constructor `#!dbuf Other`
    8. !!! danger "Currently not supported"

!!! note
    By convention every object name stats with capital letter, and every field name
    stats with lowercase letter. Consider visiting [parsing](parsing.md) documentation
    to find all rules of naming.

## Depended structures

Depended types is the key feature of *DependoBuf*.

=== "Depended `#!dbuf message`"

    ```dbuf
    message Fixed/* (1)! */ (i/*(2)!*/ Int/*(3)!*/) {
    }

    message Sample/* (4)! */ (type Int)/* (5)! */ (other Int)/* (6)! */ {
        field Int;

        f1 Fixed/* (7)! */ type/* (8)! */;
        f2 Fixed 0/* (9)! */;
        f3 Fixed field/* (10)! */;
    }
    message Example/* (11)! */ (sample Sample 1/* (12)! */ 0/* (13)! */) {
    }
    ```

    1. `#!dbuf Fixed` is an empty `#!dbuf message` that has one dependency
    2. Name of dependency
    3. Type of dependency
    4. `#!dbuf Sample` is a `#!dbuf message` that has two dependencies
    5. First dependency of `#!dbuf Sample`
    6. Second dependency of `#!dbuf Sample`
    7. `#!dbuf Sample` contains field with dependent type. Specifies 
       its dependencies with arguments separated by spaces.
    8. Dependency `#!dbuf i` of `#!dbuf Fixed` is set to be same as dependency 
       `#!dbuf type` of `#!dbuf Sample` 
    9.  Dependency `#!dbuf i` of `#!dbuf Fixed` is set to be `#!dbuf 0` 
    10. Dependency `#!dbuf i` of `#!dbuf Fixed` is set to be same as field 
        `#!dbuf field` of `#!dbuf Sample` that appears earlier than `#!dbuf f3`
    11. `#!dbuf Example` is an empty `#!dbuf message` that depends on 
        `#!dbuf Sample` with dependencies of two `#!dbuf Int`.
    12. Dependency `#!dbuf type` of `#!dbuf Sample` if set to be `#!dbuf 1` 
    13. Dependency `#!dbuf other` of `#!dbuf Sample` if set to be `#!dbuf 0` 

=== "Depended `#!dbuf enum`"

    ```dbuf 
    message Fixed/* (1)! */ (i/*(2)!*/ Int/*(3)!*/) {
    }

    enum Sample/* (4)! */ (x Int)/* (5)! */ {
        * => /* (6)! */ {
            Ctr1/* (7)! */
            Ctr2/* (8)! */ {
                y Int;
            }
            Ctr3 {
                f Fixed/* (9)!*/ x/* (10)! */;
            }
        }
    }
    ```

    1. `#!dbuf Fixed` is an empty `#!dbuf message` that has one dependency
    2. Name of dependency
    3. Type of dependency
    4. `#!dbuf Sample` is an `#!dbuf enum` that has one dependency
    5. Dependency of `#!dbuf Sample`
    6. Pattern matching syntax that explained in
       [next](#enum-pattern-matching) block
    7. Empty constructor that ignores dependency `#!dbuf (x Int)`
    8. Not empty constructor that ignores dependency `#!dbuf (x Int)`
    9.  `#!dbuf Ctr3` contains field with dependent type. Specifies 
       its dependencies with arguments separated by spaces.
    10. Dependency `#!dbuf i` of `#!dbuf Fixed` is set to be same as dependency 
        `#!dbuf x` of `#!dbuf Sample` 

## Enum pattern matching

Enum pattern matching is a way to allow using different enum constructors based
on dependencies.

### Simple pattern matching

Builtin dependencies can be matched via aliases or literals.

=== "One dependency `#!dbuf enum`"

    ```dbuf
    message Fixed (i Int) {
    }

    enum Sample (size Int)/* (1)! */ {
        x/* (2)! */ => {
            Ctr1 {
                f1 Fixed x/* (3)! */;
                f2 Fixed size/* (4)! */;
            }
        }
        1/* (5)! */ => { /* (6)! */
            Ctr1
            Ctr2
        }
        */* (7)! */ => { /* (8)! */
        }
    }
    ```

    1. Dependency `#!dbuf (size Unsigned)` for which we pattern match
    2. Aliasing, that catches every possible `#!dbuf size` and gives it alias
       name `#!dbuf x`
    3. To fulfil dependency requirements we can use alias `#!dbuf x`
    4. Also to fulfil dependency requirements we still can use `#!dbuf Sample`
       dependency `#!dbuf size`
    5. For builtin types we can use literals to pattern match on them
    6. !!! note "One pattern match might contain more than one constructor"
    7. Catch all pattern, that allows to use Its constructors for every possible
       dependencies
    8. !!! note "Pattern match might contain no constructor"
=== "Two dependencies `#!dbuf enum`"

    ```dbuf
    message Fixed (i Int) {
    }

    enum Sample (x1 Int) (x2 Int)/* (1)! */ {
        x, y/* (2)! */ => {
            Ctr1 {
                f1 Fixed x/* (3)! */;
                f2 Fixed y/* (4)! */;
            }
        }
        1, */* (5)! */ => {
            Ctr2 {
                f3 Fixed x1/* (6)! */;
                f4 Fixed x2/* (7)! */;
            }
        }
        *, 2/* (8)! */ => {
        }
        *, */* (9)! */ => {
        }
    }
    ```

    1. Pattern matching on two dependencies: `#!dbuf (x1 Int) (x2 Int)`
    2. Aliasing dependencies to names `#!dbuf x` and `#!dbuf y`
    3. Using alias `#!dbuf x` same as `#!dbuf x1`
    4. Using alias `#!dbuf y` same as `#!dbuf x2`
    5. Matching only if `#!dbuf x1` is `#!dbuf 1`
    6. Still can use `#!dbuf x1` despite the fact that it is `#!dbuf 1`
    7. Still can use `#!dbuf x2`
    8. Matching only if `#!dbuf x2` is `#!dbuf 2`
    9. Catch all pattern for multiple dependencies

### Pattern matching by constructors

Matching on `#!dbuf enum` or `#!dbuf message` might be done via constructor match.

=== "Match `#!dbuf message`"

    ```dbuf
    message Fixed (i Int) {
    }

    message RGB {
        r Int;
        g Int;
        b Int;
    }

    enum ColorMatch (c RGB)/* (1)! */ {
        RGB{r: rAlias/* (2)! */, g: *, b: */* (3)! */} => {
            Ctr {
                r1 Fixed rAlias/* (4)! */;
                r2 Fixed c.r/* (5)! */;
            }
        }

        RGB{r: rAlias, g: *, b: 0} /* (6)! */ => {
        }
    }
    ```

    1. Matching on `#!dbuf message` `#!dbuf RGB`
    2. Create alias `#!dbuf rAlias` for field `#!dbuf r` of `#!dbuf (c RGB)`
    3. Matches on every `#!dbuf g` and `#!dbuf b`
    4. Using alias `#!dbuf rAlias`
    5. Another way to access fields of `#!dbuf message`
    6. Matches only if `#!dbuf b` is `#!dbuf 0`, and creates alias
       `#!dbuf rAlias` for `#!dbuf c.r`

=== "Match `#!dbuf enum`"

    ```dbuf
    message Fixed (i Int) {
    }

    enum Color {
        Red
        Black {}
        Other {
            r Int;
            g Int;
            b Int;
        }
    }

    enum ColorMatch (c Color)/* (1)! */ {
        Red{}/* (2)! */ => {
            Ctr1 {
                r1 Fixed 255;
            }
        }
        Black{}/* (3)! */ => {
            Ctr2 {
                r2 Fixed 0; 
            }
        }
        Other{r: r, g: *, b: *}/* (4)! */ => {
            Ctr3 {
                r3 Fixed r/* (5)! */; 
            }
        }
        Other{r: r, g: *, b: 0}/* (6)! */ => {
        }
    }
    ```
    
    1. Matching on `#!dbuf enum` `#!dbuf Color`
    2. Matching on `#!dbuf Red` constructor
    3. Matching on `#!dbuf Black` constructor
    4. Matching on `#!dbuf Other` constructor, creating alias `#!dbuf r`
    5. Using alias `#!dbuf r`. Note: that is only way to access c.(as Other).r
    6. Matches only if `#!dbuf b` is `#!dbuf 0`, and creates alias `#!dbuf r`

## Constructed value

Sometimes `#!dbuf message` or `#!dbuf enum` is depends on other `#!dbuf message`
or `#!dbuf enum`. To fullfil its dependency we may force user to create field of
such type and then use that field as dependency.

```dbuf
message A {}
message ADepended (a A) {}
message Example {
    a_dep A;
    target ADepended a_dep;
}
```

That is quite inconvenient so *DependoBuf* allows using constructed value to
satisfy dependencies.

=== "Construct `#!dbuf message`"

    ```dbuf
    message Person {
        age Int;
        name String;
    }

    message Wage (p Person) {
    }

    message Example {
        num Int;
        w Wage/* (1)! */ Person{age: num/* (2)! */, name: "Steven"/* (3)! */};
    }
    ```

    1. `#!dbuf Wage` depends on `#!dbuf Person`. But there is no person in context,
       so we construct it
    2. Set field `#!dbuf age` of constructed `#!dbuf Person` equal to `#!dbuf num`
    3. Set field `#!dbuf name` of constructed `#!dbuf Person` equal to `#!dbuf "Steven"`

=== "Construct `#!dbuf enum`"

    ```dbuf
    enum Color {
        Red
        Black {}
        Other {
            r Int;
            g Int;
            b Int;
        }
    }

    enum ColorMatch (c Color) {
        /* simplified */
    }

    message ColorWarehouse {
        red ColorMatch Red{}/* (1)! */;
        other ColorMatch Other/* (2)! */{r: 12/* (3)! */, g: 0, b: 0};
    }
    ```

    1. Construct `#!dbuf Color` using empty constructor `#!dbuf Red`
    2. Construct `#!dbuf Color` using constructor `#!dbuf Other`
    3. Set field `#!dbuf r` of constructed `#!dbuf Other` equal to `#!dbuf "12"`

!!! note
    In constructed value we specify only fields of constructor, not Its dependencies
    since they are derived from type declaration.

## Compile

To compile protocol `<name.dbuf>` to programming `<languages>` use:

```bash
dbuf compile --file <name.dbuf> -o <languages>
```

That will create files with your structures, defined in DBuf, with methods to
send and receive them.

Also if you want to place such files in specific place, use `--path` flag.

## What's next?

Now that you've made it through, you have the tools to write .dbuf protocols. Consider
visiting:

* [User Guide](user_guide.md) to learn about language features.
* [Parsing](parsing.md) and [Type Checking](type_checking.md) to learn about
  language constrains.
