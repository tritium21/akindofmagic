#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='akindofmagic',
    description='File type identification using libmagic',
    author='Adam Hupp',
    author_email='adam@hupp.org',
    maintainer='Alex Walters',
    maintainer_email='tritium@sdamon.com',
    url="http://github.com/tritium21/akindofmagic",
    version='0.4.18',
    packages=find_packages(),
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    include_package_data=True,
    long_description="""This module uses ctypes to access the libmagic file type
    identification library.  It makes use of the local magic database and
    supports both textual and MIME-type output.
    """,
    keywords="mime magic file",
    license="MIT",
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
)
