#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-
"""
Go Setsuden
License: BSD

(c) 2011 ::: noriaki watanabe (nabeyang@gmail.com)
"""

from setuptools import setup

setup(name='Setsuden4Trac',
      version='0.0.1',
      packages=['setsuden4trac'],
      author='noriaki watanabe',
      author_email='nabeyang@gmail.com',
      keywords='trac setsuden',
      description='hello trac plugin',
      url='',
      license='BSD',
      zip_safe = False,
      entry_points={'trac.plugins': [
            'setsuden4trac.core = setsuden4trac.core',
            'setsuden4trac.reader = setsuden4trac.reader',]
            },
      package_data={'setsuden4trac': ['htdocs/*.gif',
                                      'htdocs/css/*.css'
                                      ]},
      exclude_package_data={'': ['tests/*']},
      test_suite = 'setsuden4trac.tests.test_suite',
      tests_require = [],
      install_requires = [])
