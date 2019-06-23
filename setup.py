from distutils.core import setup
from Cython.Build import cythonize
import numpy


setup(
        name='A-Printer Controller',
        version='2.0',
        description='A-Printer Controller based on Ivo Oasis Software',
        author='Ivo de Haas',
        maintainer='Emmanuel Arias',
        maintainer_email='eamanu@eamanu.com',
        packages=['Oasis'],
        ext_modules=cythonize(["./Oasis/ImageConverter.pyx", "./Oasis/SerialHP45.py"], annotate=False),
        include_dirs=[numpy.get_include()]
)
