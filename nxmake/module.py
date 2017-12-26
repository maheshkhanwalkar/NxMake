from typing import List, Dict
from abc import ABC, abstractmethod

from nxmake.toolchain import Toolchain
from enum import Enum
import os


# Type of object file
class ObjType(Enum):
    obj = 1
    static_lib = 2
    shared_lib = 3
    executable = 4


# Information about an object file
class ObjInfo:
    def __init__(self, target: str, obj_type: ObjType):
        self.target = target
        self.obj_type = obj_type


# Module base class
class Module(ABC):

    def __init__(self, name: str, tool: Toolchain):
        self.name = name
        self.tool = tool

    @staticmethod
    def __print_output(header: str, target: str):
        processed = str(os.path.basename(target))
        print("[" + header + "] " + processed)

    # Perform compiling
    def _do_compile(self, obj_map: Dict[str, str]) -> bool:
        for src in obj_map.keys():
            self.__print_output("CC", obj_map[src])
            result = self.tool.compile(src, obj_map[src])

            if not result:
                print(self.name + ": Compilation failed. Quitting")
                return False

        return True

    # Perform linking
    def _do_link(self, obj_src: List[ObjInfo], target: ObjInfo):

        # Build static library
        if target.obj_type is ObjType.static_lib:
            self.__print_output("AR", target.target)

            obj_raw = []

            for obj in obj_src:
                obj_raw.append(obj.target)

            result = self.tool.archive(obj_raw, target.target)

            if not result:
                print(self.name + ": Link failed. Quitting")
                return False
        else:
            # Prep output
            link_flags: List[str] = []

            # Shared library flag
            if target.obj_type is ObjType.shared_lib:
                link_flags.append("-shared")

            for obj in obj_src:
                if obj.obj_type is ObjType.executable:
                    print("Error. Cannot link executable into another file")
                    return False
                elif obj.obj_type is ObjType.obj:
                    link_flags.append(obj)
                else:
                    link_flags.append("-l:" + obj.target)

            self.__print_output("LD", target.target)
            result = self.tool.link(link_flags, target.target)

            if not result:
                print(self.name + ": Link failed. Quitting")
                return False

        return True

    @abstractmethod
    def output(self) -> List[ObjInfo]:
        pass

    @abstractmethod
    def update(self, force: bool = False) -> bool:
        pass

    @abstractmethod
    def clean(self) -> None:
        pass

    def get_name(self) -> str:
        return self.name


# Module with no modular dependencies
class BasicModule(Module):

    def __init__(self, name: str, tool: Toolchain, obj_map: Dict[str, str], target: ObjInfo = None):
        super().__init__(name, tool)
        self.obj_map = obj_map
        self.target = target

    def output(self) -> List[ObjInfo]:
        if self.target is not None:
            return [self.target]

        obj_list: List[ObjInfo] = []

        for obj in self.obj_map.values():
            obj_list.append(ObjInfo(obj, ObjType.obj))

        return obj_list

    def update(self, force: bool = False) -> bool:
        work: Dict[str, str] = {}

        if force:
            work = self.obj_map
        else:
            # Determine what needs to be compiled
            for src in self.obj_map:
                if os.path.isfile(src):
                    work[src] = self.obj_map[src]
                    continue

                # Source is newer
                if os.path.getmtime(src) > os.path.getmtime(self.obj_map[src])
                    work[src] = self.obj_map[src]

        result = super()._do_compile(work)

        if not result:
            print(self.name + ": Build failed. Quitting")
            return False

        # Perform link step (if needed)
        if self.target is not None:
            need_link: bool = False

            if os.path.exists(self.target.target) is not True:
                need_link = True
            else:
                for obj in self.obj_map.values():
                    if os.path.getmtime(obj) > os.path.getmtime(self.target.target):
                        need_link = True
                        break

            if need_link:
                obj_list: List[ObjInfo] = []

                for obj in self.obj_map:
                    obj_list.append(ObjInfo(obj, ObjType.obj))

                result = super()._do_link(obj_list, self.target)

                if not result:
                    print(self.name + ": Link failed. Quitting")
                    return False

        return True

    def clean(self) -> None:

        # Remove objects, if they exist
        for obj in self.obj_map.values():
            if os.path.isfile(obj):
                os.remove(obj)

        # Remove linked target, if there is one
        if self.target is not None:
            if os.path.isfile(self.target.target):
                os.remove(self.target.target)


class DepModule(Module):

    def __init__(self, name: str, tool: Toolchain, dep_list: List[Module], link_tgt: LinkTarget):
        super().__init__(name, tool)
        self.dep_list = dep_list
        self.link_tgt = link_tgt

    def update(self, force: bool = False) -> bool:
        print(self.name + ": Processing")

        for mod in self.dep_list:
            result = mod.update(force)

            if not result:
                print(self.name + ": Build Failed. Quiting")
                return False

        result = self._do_link()

        if not result:
            print(self.name + ": Link Failed. Quiting")
            return False

        return True

    def clean(self) -> bool:
        for mod in self.dep_list:
            result = mod.clean()

            if not result:
                return False

        return True

    def output(self) -> List[str]:
        return [self.link_tgt.get_target()]
