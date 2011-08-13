#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-
"""
Trac plugin proving a full-featured, self-contained Blog.

License: BSD

(c) 2007 ::: www.CodeResort.com - BV Network AS (simon-code@bvnetwork.no)
"""

from setuptools import setup

setup(name='Setsuden4Trac',
      version='0.0.1',
      packages=['setsuden4trac'],
      author='noriaki watanabe',
      author_email='nabeyang@gmail.com',
      keywords='trac blog',
      description='hello trac plugin',
      url='',
      license='BSD',
      zip_safe = False,
      entry_points={'trac.plugins': [
            'setsuden4trac.core = setsuden4trac.core',
            'setsuden4trac.reader = setsuden4trac.reader',]
            },
      exclude_package_data={'': ['tests/*']},
      test_suite = 'setsuden4trac.tests.test_suite',
      tests_require = [],
      install_requires = [])
