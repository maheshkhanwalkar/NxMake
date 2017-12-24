from nxmake import file

test = ["cdir/abc.c", "cppdir/def.cpp", "asmdir/xyz.s"]
result = file.outplace_map(test, "output")

for item in result:
    print(item + " -> " + result[item])