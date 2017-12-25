from typing import List, Dict

import glob
import os


def find_files(ext: str, where=None) -> List[str]:
    # Set search directory
    if where is None:
        search_dir = os.getcwd()
    else:
        search_dir = where

    prev = os.getcwd()
    os.chdir(search_dir)

    # Add starting dot, if necessary
    if ext[0] != '.':
        ext = "." + ext

    result = []

    for file in glob.glob("*" + ext):
        if search_dir[len(search_dir) - 1] is '/':
            result.append(search_dir + file)
        else:
            result.append(search_dir + "/" + file)

    # Fix current directory
    os.chdir(prev)
    return result


def default_map(src_files: List[str], where: str = None) -> Dict[str, str]:
    result = {}

    # Handle in-place vs out-of-place build mappings
    if where is None:
        for file in src_files:
            result[file] = os.path.splitext(file)[0] + ".o"

        return result
    else:
        for file in src_files:
            with_ext = str(os.path.basename(file))
            no_ext = os.path.splitext(with_ext)[0]

            if where[len(where) - 1] is '/':
                result[file] = where + no_ext + ".o"
            else:
                result[file] = where + "/" + no_ext + ".o"

        return result
