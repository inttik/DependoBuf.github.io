---
icon: "material/application-parentheses-outline"
---

# Parsing

In the top level of DBuf file exists only two types of entities:
`#!dbuf enum` and `#!dbuf message`, which are parsed one by another.

Down below such notation is used.

|     Notation     | Description                |       Example        |
| :--------------: | -------------------------- | :------------------: |
|       text       | fixed text                 |   `#!dbuf message`   |
|   `#!dbuf [x]`   | block defined elsewhere    | `#!dbuf [TypeName]`  |
| `#!dbuf !{ x }!` | zero or more times pattern | `#!dbuf !{(x Int)}!` |

Also [Backus-Naur-Form](https://en.wikipedia.org/wiki/Backus%E2%80%93Naur_form)
or BNF is used.

## Common Blocks

### Type Name

By convention every type name is a word ([a-zA-Z0-9]*) starting with uppercase letter.

So `#!dbuf Person1` and `#!dbuf Int` are `#!dbuf [TypeName]` and `#!dbuf 1field`
or `#!dbuf type` - not.

### Field Name

By convention every field or dependency name  is a word ([a-zA-Z0-9]*) starting
with uppercase letter.

So `#!dbuf name` and `#!dbuf fiELD0` are `#!dbuf [FieldName]` and `#!dbuf 1field`
or `#!dbuf Field` - not.

### Literals

`#!dbuf [Literal]` can be specified using BNF.

$$
\newcommand{or}[]{\; | \;}
\newcommand{is}[]{::=}
\newcommand{then}[]{\;}
\newcommand{block}[1]{#1}
\newcommand{ch}[1]{\texttt{#1}}
\begin{align*}
    \block{any}      &\is \text{any character expect new line} \\
    \block{any^+}    &\is \block{any} \or \block{any} \then \block{any^+}\\
    \block{string}   &\is \ch{"} \then any^+ \then \ch{"} \\
    \block{digit}    &\is \ch{0} \or \ch{1} \or \ldots \or \ch{9} \\
    \block{number}   &\is \block{digit} \or
                          \block{digit} \then \block{number} \\
    \block{int}      &\is \block{number} \\
    \block{unsigned} &\is \block{number} \then \ch{u} \\
    \block{float}    &\is \block{number} \then \ch{.} \or
                          \block{number} \then \ch{.} \then \block{number} \\
    \block{bool}     &\is \ch{true} \or \ch{false} \\
    \block{literal}  &\is \block{string} \or
                          \block{int} \or
                          \block{unsigned} \or
                          \block{float} \or
                          \block{bool} \\
\end{align*}
$$

### Expression

`#!dbuf [Expression]` is a primary expression. To specify it BNF is used.

$$
\newcommand{or}[]{\; | \;}
\newcommand{is}[]{::=}
\newcommand{then}[]{\;}
\newcommand{block}[1]{#1}
\newcommand{ch}[1]{\texttt{#1}}
\newcommand{braced}[1]{\ch{(} \then #1 \then \ch{)}}
\begin{align*}
    \block{field^+}  &\is \block{field} \or
                          \block{field} \then \ch{.} \then \block{field^+} \\
    \block{terminal} &\is \block{literal} \or
                          \block{field^+} \\
    \block{operator} &\is \ch{+} \or
                          \ch{-} \or
                          \ch{*} \or
                          \ch{/} \or
                          \ch{!} \or
                          \ch{&} \or
                          \ch{|} \\
    %
    \block{expression} &\is
    \begin{aligned}[t]
        \block{terminal} &\or
        \block{expression} \then \block{operator} \then \block{expression} \or \\
        &\or \braced{\block{expression}} \\
    \end{aligned} \\
    %
    \block{primary\_expression} &\is \block{terminal} \or
                                     \braced{\block{expression}} \or
                                     \block{constructed} \\
\end{align*}
$$

where

| Pattern       | Definition                                                |
| ------------- | --------------------------------------------------------- |
| *field*       | `#!dbuf [FieldName]`                                      |
| *literal*     | `#!dbuf [Literal]`                                        |
| *constructed* | `#!dbuf [TypeName] { !{  [FieldName] : [Expression] }! }` |

!!! note
    Nested constructed blocks such as `#!dbuf Suc{prev: Suc{prev: Zero{}}}`
    are allowed.

### Definitions

`#!dbuf [Definition]` is `#!dbuf [FieldName] [TypeName] !{ [Expression] }!`.

## Message Parsing

Messages are parsed in such way.

```dbuf
message [TypeName] !{ ( [Definition] ) }! {
    !{ [Definition] ;}!
}
```

## Enum Parsing

Enums are parsed in two different ways, depends on existing of pattern matching.

```dbuf title="No Pattern Matching"
enum [TypeName] !{ ( [Definition] ) }! {
    !{ 
    [TypeName] {
        !{ [Definition] ;}!
    } 
    }!
}
```

```dbuf title="Pattern Matching"
enum [TypeName] !{ ( [Definition] ) }! {
    !{
    [Pattern] => {
        !{
        [TypeName] {
            !{ [Definition] ;}!
        } 
        !}
    }
    }!
}
```

`#!dbuf [Pattern]` is a pattern, that can be defined as follow using BNF.

$$
\newcommand{or}[]{\; | \;}
\newcommand{is}[]{::=}
\newcommand{then}[]{\;}
\newcommand{block}[1]{#1}
\newcommand{ch}[1]{\texttt{#1}}
\begin{align*}
    \block{one\_pattern} &\is \block{field} \or
                              \block{literal} \or
                              \block{constructed\_pattern} \\
    \block{init}   &\is \block{field} \then \ch{:} \then \block{one\_pattern} \\
    \block{init^+} &\is \block{init} \or
                        \block{init} \then \ch{,} \then \block{init} \\
    \block{constructed\_pattern} &\is \block{type} \then \ch{\{} \then
                                      \block{init^+} \then \ch{\}} \\
    \block{pattern} &\is \block{one\_pattern} \or
                           \block{one\_pattern} \then
                           \ch{,} \then
                           \block{one\_pattern} \\
\end{align*}
$$

where

| Pattern   | Definition           |
| --------- | -------------------- |
| *field*   | `#!dbuf [FieldName]` |
| *literal* | `#!dbuf [Literal]`   |
| *type*    | `#!dbuf [TypeName]`  |

## Comment parsing

!!! danger
    Comments are not implemented

Comments can be linked to different objects in DependoBuf. If they are, comments
can be created for generated object. Comments can be both multi line and single
line.

```dbuf
// Comment to following message
message [TypeName] !{ ( [Definition] ) }! {
    // Comment to following field
    !{ [Definition] ;}!
}
```

```dbuf
// Comment to following enum
enum [TypeName] !{ ( [Definition] ) }! {
    !{ 
    // Comment to following constructor
    [TypeName] {
        // Comment to following field
        !{ [Definition] ;}!
    } 
    }!
}
```

```dbuf
// Comment to following enum
enum [TypeName] !{ ( [Definition] ) }! {
    !{
    [Pattern] => {
        !{
        // Comment to following constructor
        [TypeName] {
            // Comment to following field
            !{ [Definition] ;}!
        } 
        !}
    }
    }!
}
```

!!! warning
    Even if it is possible to create comment if other places of file
    it is not recommended since after formatting their fate is undefined.
