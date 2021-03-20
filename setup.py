import os
import sys

from setuptools import find_packages, setup

VERSION = "0.1"

if sys.version_info[:2] < (3, 6):
    raise RuntimeError("Python version >= 3.6 required.")

setup(
    name='pyBittle',
    version=VERSION,
    description='pyBittle package',
    url='https://github.com/EnriqueMoran/pyBittle',
    author='EnriqueMoran',
    author_email='enriquemoran95@gmail.com',
    install_requires=['pybluez', 'pyserial'],
    packages=find_packages(),
    zip_safe=False,
)
