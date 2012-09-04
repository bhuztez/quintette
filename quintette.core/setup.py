#!/usr/bin/env python2

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import os.path
import pkgutil


def find_packages(path=None, prefix=''):
    path = path or [os.path.dirname(os.path.abspath(__file__))]
    packages = []

    for loader, name, ispkg in pkgutil.iter_modules(path, prefix):
        if ispkg:
            packages.append(name)
            packages.extend(
                find_packages(
                    [ os.path.join(loader.path, name) ],
                    name+'.'))

    return packages


PACKAGES = find_packages()


setup(
    name='quintette.core',
    version='0.0',

    url='https://github.com/bhuztez/quintette',
    description='yet another collection of Django apps',

    classifiers = [
        "Development Status :: 1 - Planning",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],

    author='bhuztez',
    author_email='bhuztez@gmail.com',

    requires=['Django (>= 1.4)'],

    namespace_packages = ['quintette'],

    packages = PACKAGES,

    zip_safe = False,
)


