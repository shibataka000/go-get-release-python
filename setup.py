"""
distutils/setuptools install script
"""

import os
from setuptools import setup, find_packages


def find_install_requires():
    """
    Find install_requires from requirements.txt
    """
    path = os.path.join(os.path.dirname(__file__), "requirements.txt")
    return [x.strip() for x in open(path) if not x.startswith("#")]


setup(
    name="go-get-release",
    version="0.0.1",
    description="",
    author="shibataka000",
    url="https://github.com/shibataka000/go-get-release",
    packages=find_packages(),
    install_requires=find_install_requires(),
    license="MIT",
    scripts=["bin/go-get-release"],
)
