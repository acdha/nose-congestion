===============
nose-congestion
===============

Nose can report test execution time in its various output formats but it
doesn't include the `setUp` or `tearDown` time, which can be substantial.

.. image:: https://travis-ci.org/acdha/nose-congestion.svg?branch=master   :target: https://travis-ci.org/acdha/nose-congestion

Usage
-----

1. ``pip install nose-congestion``
2. ``nosetests --with-congestion``

Output
------

After all of the tests complete, a simple table will be printed::

    Location                                       Total    setUp tearDown
    ----------------------------------------------------------------------
    module.tests.FastTests                         7.187    1.659    0.000
    module.tests.SlowTests                         0.047    0.002    0.000

      Total  Location
    ----------------------------------------------------------------------
      0.104  module.tests.SlowTests.test_method
      0.009  module.tests.FastTests.test_method

Requirements
------------

* nose
* Python 2.6+, Python 3.3+
