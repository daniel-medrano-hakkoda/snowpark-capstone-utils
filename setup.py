from setuptools import setup, find_packages

__version__ = '0.1.0'

setup(
    name='snowpark-capstone-utils',
    version=__version__,

    url='https://github.com/daniel-medrano-hakkoda/snowpark-capstone-utils',
    author='Daniel Medrano',
    author_email='daniel_medrano@hakkoda.io',

    packages=find_packages(),

    install_requires=[
        'snowflake-snowpark-python',
    ],
)