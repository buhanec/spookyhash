from Cython.Build import cythonize
from setuptools import Extension, setup


setup(
    ext_modules=cythonize(
        [
            Extension(
                '_spookyhash',
                ['src/spookyhash.pyx', 'src/SpookyV2.cpp'],
                language='c++',
            ),
        ],
        compiler_directives={
            'embedsignature': True,
            'language_level': 3,
        },
    ),
)
