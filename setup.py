# encoding: utf-8
from __future__ import absolute_import, print_function, unicode_literals

import os
import sys

from setuptools import setup

ROOT = os.path.dirname(__file__)

setup(name='nose-congestion',
      version='0.0.3',
      author='Chris Adams',
      author_email='chris@improbable.org',
      url='http://github.com/acdha/nose-congestion',
      description='Find slow test setUp/tearDown',
      long_description=open(os.path.join(ROOT, 'README.rst')).read(),
      py_modules=['nose_congestion'],
      include_package_data=True,
      zip_safe=False,
      entry_points={
          'nose.plugins.0.10': [
              'congestion = nose_congestion:CongestionPlugin',
          ]
      },
      setup_requires=['nose>=1.0'],
      test_suite = 'nose.collector')
