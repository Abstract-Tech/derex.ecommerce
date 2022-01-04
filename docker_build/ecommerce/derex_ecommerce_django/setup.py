"""Derex support egg.
This egg is meant to be installed automatically by ``derex`` alongside
``ed-platform``. End users sould never need to install this.
"""
from setuptools import find_packages
from setuptools import setup


setup(
    name="derex_ecommerce_django",
    version="0.0.1",
    description="Support package for derex",
    url="http://github.com/Abstract-Tech/derex.ecommerce",
    author="Chiruzzi Marco",
    author_email="chiruzzi.marco@gmail.com",
    license="AGPL",
    packages=find_packages(),
    zip_safe=False,
    entry_points={},
)
