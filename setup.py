"""Minimal setup.py shim for backward compatibility with older toolchains.

All configuration is in pyproject.toml. This file exists only so that
`python setup.py install` and similar legacy commands still work.
"""

from setuptools import setup

setup()
