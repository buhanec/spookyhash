from Cython.Build import cythonize
from setuptools import Extension, setup

setup(
    ext_modules=cythonize(
        [
            Extension(
                "spookyhash._spookyhash",
                ["src/spookyhash.pyx", "src/SpookyV2.cpp"],
                language="c++",
            ),
        ],
        compiler_directives={
            "cdivision": True,
            "boundscheck": False,
            "wraparound": False,
            "embedsignature": True,
            "language_level": 3,
            "freethreading_compatible": True,
        },
    ),
)
