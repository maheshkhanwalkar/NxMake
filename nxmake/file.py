import glob
import os
from typing import List, Dict


def find_files(extension: str) -> List[str]:
    # File files in the current directory with the extension: 'extension'
    return find_files_in(os.getcwd(), extension)


def find_files_in(directory : str, extension: str) -> List[str]:
    # Find files in 'directory' with extension: 'extension'
    result = []
    os.chdir(directory)

    for file in glob.glob("*" + extension):
        result.append(directory + "/" + file)

    return result


def inplace_map(files: List[str]) -> Dict[str, str]:
    # Create a default mapping of *.{c,cpp,...} to *.o (inplace build)
    result = {}
    for file in files:
        result[file] = os.path.splitext(file)[0] + ".o"

    return result


def outplace_map(files : List[str], build_dir : str) -> Dict[str, str]:
    # Create a mapping of *.{c,cpp,...} to build_dir/*.o (out-of-place build)
    result = {}

    for file in files:
        f_name_ext = str(os.path.basename(file))
        f_name_none = os.path.splitext(f_name_ext)[0]

        result[file] = build_dir + "/" + f_name_none + ".o"

    return result
