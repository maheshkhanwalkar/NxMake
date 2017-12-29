# NxMake
#### Customizable Build System

NxMake is similar to SCons in the sense that configuration is done using a
Python script. However, a major difference, is that with NxMake is actually just
a library: that is, the configuration script actually is run directly!

The problem with most build systems is that the user is forced to do things a
certain way, to conform to the build system; however, a build system should
work with the user's needs.

Since NxMake is a library, it does just that: it provides a set of useful
classes and methods; however, there is no compulsion or lock-in into using
every component.

Don't like the default src to obj mapping, or need something more powerful?
Write whatever you need and just provide NxMake the custom src to obj map and
it will handle the compile and link phase as expected.

#### How to install:

NxMake is hosted on PyPI, so it can easily be installed using
pip. NxMake requires Python 3; however, has no other dependencies. The current
build is 1.0.0a1

```bash
pip3 install --user NxMake
```

#### Resources:

Checkout the `docs/` directory for an extensive documentation and feature
enumeration, as well as, useful tutorials to get started.

Some quick tutorial links:

* [Getting started](doc/tutorials/GettingStarted.md)
* [Customizing the build process](doc/tutorials/CustomizeBuild.md)
* Working with modules
