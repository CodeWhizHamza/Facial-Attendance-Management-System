from setuptools import setup
from Cython.Build import cythonize

setup(
	name='AMS',
	ext_modules=cythonize('main.py'),
	zip_safe=False
)