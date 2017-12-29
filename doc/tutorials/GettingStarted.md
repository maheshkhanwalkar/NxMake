# Getting Started

#### Basic Overview

NxMake is a library, so there is no *executable* provided by the build system.
The philosophy is that the build should begin and end with the user. So the
configuration script is the *executable* that is run.

The configuration script is actually just a Python 3 script that uses NxMake
to simplify various low-level tasks required in build systems. This allows
the user to structure their build flow the way that they want to, rather than
forcing it to work with the peculiarities of a certain build system.

#### Simple Example
Let's get started with a simple example:

```c
/* example1.c */
#include <stdio.h>

int main(int argc, const char* argv[])
{
    printf("Hello world\n");
    return 0;
}
```
There is only one file to build, **example1.c**. It probably is overkill to
need a build system for just one file; however, let's just see how it would
look.

```python
# build.py (although the name doesn't actually matter)
from nxmake.toolchain import Toolchain, default_toolchain
from nxmake.module import BasicModule, ObjInfo, ObjType

# Grab the default toolchain
tool = default_toolchain()

# Construct a module (name, toolchain, src -> obj dictionary, output)
mod = BasicModule("Example1_Mod", tool, {"example1.c" : "example1.o"},
          ObjInfo("example1", ObjType.executable))

# Perform the build (if there is something to do)
mod.update()
```

To run the build just do: `python3 build.py`. As stated earlier, the
configuration script is run directly.

Even from this simple example, there seems to be a lot going on, which is
accurate. However, even with complex examples, there is not much else in
addition to this.

Let's break it down line-by-line to get a sense of what is going on:

#### Basic Components

The build itself contains a few main components: the toolchain, the modules,
the source-to-object mapping, and the output. Even in this simple example, all
parts of the build are shown (albeit in a simple way)

##### Constructing the Toolchain

```python
# Get the default toolchain
tool = default_toolchain()
```

The toolchain consists of the compiler and linker, but could also have an
archiver to handle static libraries. In this example, there is no need for a
custom toolchain, so we just get the default one.

##### Source to Object Mapping

NxMake needs to know what sources to build and where to place the results. The
source-to-object mapping is a flexible way to describe that information.

Effectively, it is a dictionary, which contains a mapping from a source file
path to an object file path, which allows for in-place, out-of-place, and
complex build patterns.

```python
{"example1.c" : "example1.o"}
```
This represents the source-to-object map. It says there is a file:
**example1.c** that should be mapped to **example1.o**. So this is a simple,
in-place build of one source file.

##### Specifying Build Output

There are a few kinds of object outputs: object files, static libraries,
shared libraries, and executables. NxMake needs to know what is the end result
of the build and what type it is, so as to run the correct link step.

In this example, that is specified with:

```python
ObjInfo("example1", ObjType.executable)
```
This creates an instance of ObjInfo, which contains the target output path
as well as its type. We want to build an executable called **example1** as
the output of this build. Needing to build multiple outputs or not having
any outputs is the subject of the Module series of classes.

##### Constructing Modules

Modules are an important component of NxMake. They represent small, packaged
components that can be built. In this example, a `BasicModule` is used, which
is one of currently two types of modules.

A BasicModule essentially is a module that does not depend on any other
modules: it just depends on source files, which is why it is used in this
example. There is no need for a more complex module here.

```python
# Construct a module (name, toolchain, src -> obj dictionary, output)
mod = BasicModule("Example1_Mod", tool, {"example1.c" : "example1.o"},
          ObjInfo("example1", ObjType.executable))
```

This creates a BasicModule with name **Example1_Mod**, that uses the default
toolchain (see above), with a source-to-object mapping (see above) with a module
output, the executable **example1** (see above)

The module output is actually an optional parameter, since not all modules will
need a link step. However, there is only one module here, so there probably
should be a module output.

##### Building Modules

Once a module is constructed, it can be built. The Module determines what needs
to be built, based on what is out-of-date. The `update()` operation will be
effectively a no-op if there is nothing to do.

```python
# Perform the build (if there is something to do)
mod.update()
```

This will perform the build. The equivalent commands that would be executed in
this example:

```bash
cc -c example1.c -o example1.o
cc -o example1 example1.o
```

What C compiler would be invoked depends on what is the default compiler flag
of the executing environment, that is what the **CC** environmental variable
is set to. If it isn't set, then NxMake guesses: **cc** in **$PATH**, which
ideally should exist.

#### Next Tutorial
* [Customizing the build process](CustomizeBuild.md)

#### Documentation:
* Module documentation
* Toolchain documentation
