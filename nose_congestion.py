# encoding: utf-8
from __future__ import absolute_import, print_function

import operator
import os
from functools import wraps
from inspect import ismodule
from time import time

from nose.plugins import Plugin


class CongestionPlugin(Plugin):
    """Measure total test execution time"""
    name = 'congestion'

    def __init__(self):
        super(CongestionPlugin, self).__init__()
        self.start_times = {}
        self.elapsed_times = {}
        self.timed_tests = {}

    @staticmethod
    def name_for_obj(i):
        if ismodule(i):
            return i.__name__
        else:
            return "%s.%s" % (i.__module__, i.__name__)

    def record_elapsed_decorator(self, f, ctx, key_name):
        @wraps(f)
        def wrapped(*args, **kwargs):
            start_time = time()

            try:
                return f(*args, **kwargs)
            finally:
                ctx[key_name] = time() - start_time

        return wrapped

    def options(self, parser, env=os.environ):
        super(CongestionPlugin, self).options(parser, env=env)

    def configure(self, options, conf):
        super(CongestionPlugin, self).configure(options, conf)
        if not self.enabled:
            return

    def startContext(self, context):
        ctx_name = self.name_for_obj(context)
        self.elapsed_times[ctx_name] = ctx = {'total': 0, 'setUp': 0,
                                              'tearDown': 0}

        if hasattr(context, 'setUp'):
            for k in ('setUp', 'tearDown'):
                old_f = getattr(context, k)
                new_f = self.record_elapsed_decorator(old_f, ctx, k)
                setattr(context, k, new_f)

        self.start_times[context] = time()

    def stopContext(self, context):
        end_time = time()

        elapsed = end_time - self.start_times.pop(context)
        ctx_name = self.name_for_obj(context)
        self.elapsed_times[ctx_name]['total'] = elapsed

    def startTest(self, test):
        self._timer = time()

    def _register_time(self, test):
        self.timed_tests[test.id()] = self._timeTaken()

    def _timeTaken(self):
        if hasattr(self, '_timer'):
            return time() - self._timer
        else:
            # Test died before it ran (probably error in setup()) or
            # success/failure added before test started probably due to custom
            # TestResult munging.
            return 0.0

    def addError(self, test, err, capt=None):
        self._register_time(test)

    def addFailure(self, test, err, capt=None, tb_info=None):
        self._register_time(test)

    def addSuccess(self, test, capt=None):
        self._register_time(test)

    def report(self, stream):
        print("%-43s %8s %8s %8s" % ('Location', 'Total', 'setUp', 'tearDown'),
              file=stream)
        print('-' * 70, file=stream)

        fmt = "{0:43s} {total:>8.3f} {setUp:>8.3f} {tearDown:>8.3f}"
        for context_name in sorted(self.elapsed_times.keys()):
            times = self.elapsed_times[context_name]
            print(fmt.format(context_name, **times), file=stream)

        print(file=stream)
        print("%7s  %-60s" % ('Total', 'Location'), file=stream)
        print('-' * 70, file=stream)

        fmt = "{0[1]:>7.3f}  {0[0]:60s}"

        for timed in sorted(self.timed_tests.items(),
                            key=operator.itemgetter(1), reverse=True):
            print(fmt.format(timed), file=stream)
