from setuptools import setup, Extension

setup(
    ext_modules=[Extension("name of your library", ["path to the C folder"])]
)
