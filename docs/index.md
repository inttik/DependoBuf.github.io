---
icon: "lucide/rocket"
---

# Introduction

DependoBuf is a novel structured data serialization format that incorporates
dependent types into the data model. It is designed to be a more expressive and
safe alternative by providing the ability to describe not only the structure of
the data, but the relationships between the data as well and enforcing those
relationships at both compile and runtime.

Consider transmission of binary tree as example.
=== "Protocol Buffers"

    <div class="grid" markdown>
    <div markdown>
    ```protobuf
    message TreeH {
        message TreeHLeaf {
            int32 value = 1;
            uint32 height = 2;
        }

        message TreeHNode {
            int32 value = 1;
            uint32 height = 2;
            TreeH left = 3;
            TreeH right = 4;
        }

        oneof treeh_type {
            TreeHLeaf leaf = 1;
            TreeHNode node = 2;
        }
    }
    ```

    </div>
    <div style="margin: 16px;" markdown>
    :heavy_multiplication_x: Constraints not obvious

    :heavy_multiplication_x: No way to define constraints in schema

    :heavy_multiplication_x: No way to validate constraints soundness

    :heavy_multiplication_x: Need to write custom code to validate constraints
    </div>
    </div>

=== "DependoBuf"

    <div class="grid" markdown>
    <div markdown>
    ```dbuf
    enum TreeH (height Unsigned) {
        0 => {
            TreeHLeaf {
                value Int
            }
        }
        * => {
            TreeHNode {
                value Int
                left TreeH (height - 1)
                right TreeH (height - 1)
            }
        }
    }
    ```

    !!! danger
        Names of builtin types are not fixed, so the code
        might be incorrect.

    </div>
    <div style="margin: 16px;" markdown>
    :heavy_check_mark: Obvious constraints

    :heavy_check_mark: Constraint definition in schema

    :heavy_check_mark: Soundness validation at compile time

    :heavy_check_mark: Automatic validation of constraints at runtime
    </div>
    </div>

## Documentation pages

* [Installation](install.md) documentation to install DependoBuf.
* [Get Started](get_start.md) documentation to write simple serialization protocols.
* [User Guide](user_guide.md) documentation to check language capabilities.
* [Parsing](parsing.md) documentation to learn how protocol is parsing in detail.
* [Type Checking](type_checking.md) documentation to find out how protocols
  guarantees are maintained.

!!! warning
    The project is work in progress. The language and its features might change.

## Documentation progress

* [X] intro page
* [X] user download page
* [X] get start
* [X] user docs
* [X] parsing
* [ ] type checks
