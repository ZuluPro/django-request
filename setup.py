#!/usr/bin/env python
from setuptools import setup, find_packages
import request


def read_file(name):
    with open(name) as fd:
        return fd.read()

setup(
    name='pony-traffic',
    version=request.__version__,
    description=request.__doc__,
    long_description=read_file('README.rst'),
    author=request.__author__,
    author_email=request.__email__,
    url=request.__url__,
    download_url=request.__download__,
    include_package_data=True,
    packages=find_packages(exclude=['tests']),
    install_requires=read_file('requirements.txt'),
    license=request.__licence__,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Natural Language :: English',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ]
)
