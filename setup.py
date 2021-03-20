import setuptools

VERSION = "0.1"

setuptools.setup(
    name='pyBittle',
    version=VERSION,
    description='pyBittle package',
    url='https://github.com/EnriqueMoran/pyBittle',
    author='EnriqueMoran',
    install_requires=['pybluez', 'pyserial'],
    author_email='enriquemoran95@gmail.com',
    packages=setuptools.find_packages(),
    zip_safe=False
)