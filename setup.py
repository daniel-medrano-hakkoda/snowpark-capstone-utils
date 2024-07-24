from setuptools import setup

from connection import __version__

setup(
    name='snowpark_capstone_utils',
    version=__version__,

    url='https://github.com/daniel-medrano-hakkoda/snowpark-capstone-utils',
    author='Daniel Medrano',
    author_email='daniel_medrano@hakkoda.io',

    py_modules=['connection'],
)