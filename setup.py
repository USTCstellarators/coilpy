import os
import setuptools
from setuptools import Extension, setup

# fortran compiler
compiler = os.environ.get('FC', 'gfortran')  # replace 'gnu95' with your default compiler
# set some fortran compiler-dependent flags
f90flags = []
if compiler == "gnu95":
    f90flags.append("-ffree-line-length-none")
else:
    pass

f90flags.append("-O3")

ext = Extension(
    name="coilpy_fortran",
    sources=[
        "coilpy/fortran/biotsavart.f90",
    ],
    extra_compile_args=f90flags,
)

setup(
    packages=setuptools.find_packages(),
    ext_modules=[ext],
)
