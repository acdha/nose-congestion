# encoding: utf-8
from __future__ import absolute_import

from inspect import ismodule
from functools import wraps
from time import time
import os

from nose.plugins import Plugin


class CongestionPlugin(Plugin):
    """Measure total test execution time"""
    name = 'congestion'

    def __init__(self):
        super(CongestionPlugin, self).__init__()
        self.start_times = {}
        self.elapsed_times = {}

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

    def report(self, stream):
        print >>stream, "%-43s %8s %8s %8s" % ('Location', 'Total',
                                               'setUp', 'tearDown')
        print >>stream, '-' * 70

        fmt = "{0:43s} {total:>8.3f} {setUp:>8.3f} {tearDown:>8.3f}"
        for context_name in sorted(self.elapsed_times.keys()):
            times = self.elapsed_times[context_name]
            print >>stream, fmt.format(context_name, **times)
