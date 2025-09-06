This is how to use it... (duhhz :3)

To use the already compiled version the one named (mymenu.cpython-313-x86_64-linux-gnu.so)
just put it in the same python folder as your project then just add a import at the top 

vv Python
import mymenu

Now for the uncompiled version thats straight code you gotta make setup.py file like this

vv Python
from setuptools import setup, Extension

setup(
    ext_modules=[Extension("name of the library", ["path to the uncompiled .c library"])]
)

Then run this command in terminal

vv Terminal
python3 setup.py build_ext --inplace


Hope this helps ^w^ I just wanna help everyone else whom is learning code aswell
