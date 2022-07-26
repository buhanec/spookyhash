from Cython.Build import cythonize
from setuptools import Extension, setup


setup(
    name="spookyhash",
    url="https://github.com/buhanec/spookyhash",
    ext_modules=cythonize(
        [
            Extension(
                '_spookyhash',
                ['src/spookyhash.pyx', 'src/SpookyV2.cpp'],
                language='c++',
            ),
        ],
        compiler_directives={
            "cdivision": True,
            "boundscheck": False,
            "wraparound": False,
            'embedsignature': True,
            'language_level': 3,
        },
    ),
)
