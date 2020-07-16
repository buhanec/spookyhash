from Cython.Build import cythonize
from setuptools import Extension, find_packages, setup

with open('README.md') as f:
    long_description = f.read()

setup(
    name='spookyhash',
    version='2.0.0',
    author='Alen Buhanec',
    author_email='<alen.buhanec@gmail.com>',
    license='MIT',
    description='A Python wrapper for SpookyHash version 2',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/buhanec/spookyhash',
    classifiers=[
        'Topic :: Software Development :: Libraries',
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Typing :: Typed',
    ],
    include_package_data=True,
    ext_modules=cythonize([
        Extension('spookyhash',
                  ['src/spookyhash.pyx', 'src/SpookyV2.cpp'],
                  language='c++'),
    ], compiler_directives={'embedsignature': True}),
)
