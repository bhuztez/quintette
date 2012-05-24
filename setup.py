#!/usr/bin/env python2

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='quintette',
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

    namespace_packages = ['quintette', 'quintette.contrib'],
    packages=[
        'quintette',
        'quintette.conf',
        'quintette.core',
        'quintette.core.templatetags',
        'quintette.db',
        'quintette.db.models',
        'quintette.http',

        'quintette.contrib',
        'quintette.contrib.accounts',
        'quintette.contrib.avatar',
        'quintette.contrib.avatar.templatetags',
    ],

    zip_safe = False,
)


