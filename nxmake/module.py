from typing import List, Dict
from abc import ABC, abstractmethod

from nxmake.toolchain import Toolchain
import os


# Module base class
class Module(ABC):

    def __init__(self, name: str, tool: Toolchain):
        self.name = name
        self.tool = tool

    @abstractmethod
    def output(self) -> List[str]:
        pass

    @abstractmethod
    def update(self) -> bool:
        pass

    def get_name(self) -> str:
        return self.name


# Module with no modular dependencies
class BaseModule(Module):

    def __init__(self, name: str, obj_map: Dict[str, str], tool: Toolchain, link_target: str = None):
        super().__init__(name, tool)
        self.obj_map = obj_map
        self.link_target = link_target

    def output(self) -> List[str]:
        if not (self.link_target is None):
            return [self.link_target]

        return list(self.obj_map.values())

    @staticmethod
    def __print_output(header: str, target: str):
        processed = str(os.path.basename(target))
        print("[" + header + "] " + processed)

    # Perform the compile step
    def __do_compile(self, update_list: List[str]) -> bool:
        for src in update_list:
            self.__print_output("CC", self.obj_map[src])
            result = self.tool.compile(src, self.obj_map[src])

            if not result:
                print(self.name + ": Compilation failed. Quiting")
                return False

        return True

    # Perform the link step, if there is one
    def __do_link(self) -> bool:
        if self.link_target is not None:
            print(self.name + ": Linking")

            self.__print_output("LD", self.link_target)
            result = self.tool.link(list(self.obj_map.values()), self.link_target)

            if not result:
                print(self.name + ": Linking failed. Quiting")
                return False

        return True

    def update(self, force: bool = False) -> bool:
        # Force recompile (and possibly relink)
        if force:
            print(self.name + ": Compiling")
            result = self.__do_compile(list(self.obj_map.keys()))

            if not result:
                return False

            result = self.__do_link()

            if not result:
                return False

            return True

        # Determine what needs to be updated
        update_list = []

        for src in self.obj_map.keys():
            if not os.path.exists(src):
                print(self.name + ": Error. " + src + " does not exist")
                return False

            src_time = os.path.getmtime(src)

            if not os.path.exists(self.obj_map[src]):
                update_list.append(src)
                continue

            tgt_time = os.path.getmtime(self.obj_map[src])

            # Need to update
            if src_time > tgt_time:
                update_list.append(src)

        # There is something to update
        if len(update_list) != 0:
            print(self.name + ": Compiling")

            result = self.__do_compile(update_list)

            if not result:
                return False

            result = self.__do_link()

            if not result:
                return False

        else:
            print(self.name + ": Nothing to update")

        return True

    def clean(self) -> bool:
        for obj in self.obj_map.values():
            if not os.path.isfile(obj):
                return False
            os.remove(obj)

        # Remove linked target, if there is one
        if not (self.link_target is None):
            if not os.path.isfile(self.link_target):
                return False
            os.remove(self.link_target)

        return True
