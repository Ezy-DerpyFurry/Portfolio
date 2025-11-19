This is the raw c++ code to the terminalUiLibrary so yea... again read the LICENSE before you do stuff with it.

You can compile the code with

g++ -O3 -std=c++20 -fPIC -shared \
    $(python3-config --includes) \
    terminalui.cpp \
    -o terminalui$(python3-config --extension-suffix)
