import os
import pathlib
import sys

from setuptools import find_packages, setup

VERSION = "1.0.0"
DIR = pathlib.Path(__file__).parent
README = (DIR / "README.md").read_text()

if sys.version_info[:2] < (3, 6):
    raise RuntimeError("Python version >= 3.6 required.")

setup(
    name='pyBittle',
    version=VERSION,
    description='Open source library for connecting and controlling Bittle.',
    long_description=README,
    long_description_content_type="text/markdown",
    url='https://github.com/EnriqueMoran/pyBittle',
    author='EnriqueMoran',
    author_email='enriquemoran95@gmail.com',
    install_requires=['pybluez', 'pyserial', 'requests'],
    packages=find_packages(),
    zip_safe=False,
)
