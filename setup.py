#!/usr/bin/env python
from setuptools import setup, find_packages
import fborm

setup(
    name="fogbugz-orm",
    version=fborm.__version_string__,
    description="FogBugz API Object Relational Mapper (ORM)",
    long_description=open('README.rst').read(),
    url="https://github.com/dougn/fogbugz-orm/",
    author=fborm.__author__,
    author_email=fborm.__email__,
    license="BSD",
    packages=["fborm"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: BSD License",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires=['fogbugz', 'jsontree'],
    keywords=["fogbugz", "api", "orm"],
)