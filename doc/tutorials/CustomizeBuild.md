# Customizing the Build

#### Default Options

In the [Getting Started](GettingStarted.md) tutorial, the default toolchain was
utilized; however, that isn't always useful. In fact, most users who are
building more than one file, would want to be able to customize the build.

There are multiple levels of customizability, because each major component of
NxMake can configured to meet the needs of the build flow.

This tutorial will break it down into two major components:
* Source to Object Mapping
* Toolchain Customization

##### Source to Object Mapping

NxMake makes the mapping of source to compiled object extremely flexible, by
providing reasonable defaults, but letting the build system user configure their
own.

The Getting Started tutorial did not use any of the default mappings, because
the mapping was so simple: just one source file. However, NxMake provides one
useful function to handle two kinds of mappings:

###### In-Place Build:
```python
from nxmake.file import default_map
obj_map = default_map(src_list)
```

`default_map()` takes a `List[str]`, which is the list of source files and
returns a `Dict[str, str]` which maps each entry of the source list to an
object file, via the rule: `some-path/src.{some-ext} -> some-path/src.o`

###### Out-of-Place Build:
```python
from nxmake.file import default_map
obj_map = default_map(src_list, "build/")
```
`default_map()` takes a `List[str]`, the list of source files and now also
takes a build directory path, returning a dictionary which maps each
entry of the source list to an object file, via the rule:
`some-path/src.c -> build/src.o`

This provides a simple, out-of-place build. However, it is not all-catching. If
there are duplicate source file names, then it won't work as expected, since it
does not respect subdirectory structure. This is something that will eventually
be supported.

###### Custom Build:

Although NxMake has a direct function to handle in-place and simple out-of-place
builds, it can also work with a more sophisticated (or at least different)
custom build flow.

The reason behind returning a map `Dict[str, str]` is to allow the build system
user to provide their own mapping, if the defaults are not suitable. Therefore,
the user can write their own function(s) to build the mapping and then pass that
map to a module to build the source accordingly.

##### Toolchain Customization

NxMake allows for complete toolchain customization, but also provides a default
one for simplicity. The Getting Started tutorial made use of the default
toolchain; however, most builds will need some level of customization.

###### Default Toolchain

```python
from nxmake.toolchain import default_toolchain
tool = default_toolchain()
```

This snippet gets the default toolchain, which relies on system defaults and
environment variables. It checks to see if **CC** is set, otherwise guessing
for **cc** in path (e.g. /usr/bin/cc). This probably isn't what most people
want.

###### Custom Components

The compiler, linker, and archiver tools can all be customized to generate a
custom toolchain instance. The classes `Compiler`, `Linker`, and `Archiver`
encapsulate the functions of their respective executables.

The code to pass in custom components for a custom toolchain is quite simple and
straightforward:

```python
from nxmake.toolchain import Compiler, Linker, Archiver, Toolchain

cc = Compiler("clang++", "-Wall -Wextra -std=c++14 -stdlib=libc++".split(" "))
ld = Linker("clang++", "-fuse-ld=lld -stdlib=libc++".split(" "))
ar = Archiver("llvm-ar", ["rcs"])

tool = Toolchain(cc, ld, ar)
```
This snippet gives a practical demonstration of a `llvm/clang`-only toolchain,
as it specifies the use of `clang++` for C++ compiler, `libc++` for the C++
standard library, `clang++` as the linker (with the use of `lld` internally),
and `llvm-ar` for archiving.

In addition, a `verbose` flag can be set to explicitly print out the actual
commands being executed. It can be passed to a component of the toolchain
individually (if only some components should have verbose output):

```python
from nxmake.toolchain import Compiler, Linker, Archiver, Toolchain

# Compiler-only verbose output
cc = Compiler("clang++", [...], True)
ld = Linker(...)
ar = Archiver(...)

tool = Toolchain(cc, ld, ar)
```
or to the toolchain as a whole:
```python
from nxmake.toolchain import Compiler, Linker, Archiver, Toolchain

cc = Compiler(...)
ld = Linker(...)
ar = Archiver(...)

# Toolchain-wide verbose output
tool = Toolchain(cc, ld, ar, True)
```

#### Next Tutorial
* Working with Modules

#### Documentation:
* Toolchain documentation
