#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(name='akindofmagic',
      description='File type identification using libmagic',
      author='Adam Hupp',
      author_email='adam@hupp.org',
      maintainer='Alex Walters',
      maintainer_email='tritium@sdamon.com',
      url="http://github.com/tritium21/akindofmagic",
      version='0.4.13',
      py_modules=['magic'],
      long_description="""This module uses ctypes to access the libmagic file type
identification library.  It makes use of the local magic database and
supports both textual and MIME-type output.
""",
      keywords="mime magic file",
      license="MIT",
      test_suite='test',
      classifiers=[
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
      ],
      )
