#!/usr/bin/env python3

from setuptools import setup, find_packages

long_description = """
# fonts-offline
Take fonts from google fonts and convert them for offline use.
"""

setup(
    name='fonts-offline',
    version='0.1.0',
    description='Download fonts and create css to import them',
    long_description=long_description,
    author='Marco "don" Kaulea',
    author_email='don@0xbeef.org',
    url='https://github.com/Don42/fonts-offline',
    packages=find_packages(),
    install_requires=['pathlib', 'docopt', 'requests'],
    classifiers=[],
    scripts=['fonts-offline.py'],
)
