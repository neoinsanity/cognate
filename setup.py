"""The setuptools setup file."""
from setuptools import setup

with open('README.txt') as file:
    long_description = file.read()

setup(
    name='cognate',
    version='0.0.1',
    author='Raul Gonzalez',
    author_email='mindbender@gmail.com',
    url='https://github.com/neoinsanity/cognate',
    license='Apache License 2.0',
    description='From the same root',
    long_description=long_description,
    packages=['cognate',],
    install_requires=[],
    include_package_data = True,
)

