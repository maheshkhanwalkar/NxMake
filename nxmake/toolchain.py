from subprocess import call
from typing import List


class Compiler:
    def __init__(self, cc_exe: str, flags: List[str]):
        self.cc_exe = cc_exe
        self.flags = flags

    def compile(self, src: str, target: str) -> bool:
        return call([self.cc_exe, *self.flags, "-c", src, "-o", target]) == 0

    def cmd_str(self, src: str, target: str) -> str:
        return self.cc_exe + " " + ' '.join(self.flags) + " -c " + src + " -o " + target


class Linker:
    def __init__(self, ld_exe, flags: List[str]):
        self.ld_exe = ld_exe
        self.flags = flags

    def link(self, obj: List[str], target: str) -> bool:
        return call([self.ld_exe, *self.flags, *obj, "-o", target]) == 0


class Toolchain:
    def __init__(self, cc: Compiler, ld: Linker):
        self.cc = cc
        self.ld = ld

    def compile(self, src: str, target: str) -> bool:
        return self.cc.compile(src, target)

    def link(self, obj: List[str], target: str) -> bool:
        return self.ld.link(obj, target)