#! /usr/bin/python3.5

from distutils.core import setup
from Cython.Build import cythonize
from distutils.extension import Extension


ext_modules = [
    Extension("individu",
	sources=["individu.pyx"],
    libraries=["m"]
    ),
    Extension("population",
    sources=["population.pyx"],
    libraries=["m"])
]

setup(
    name="Interface",
    ext_modules=cythonize(ext_modules),
)
