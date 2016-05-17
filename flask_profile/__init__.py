# -*- coding: utf-8 -*-
"""
    flaskext.profile
    ~~~~~~~~~~~~~~~~

    Adds profiling to Flask.

    :copyright: (c) 2014 by Shipeng Feng.
    :license: BSD, see LICENSE for more details.
"""

import pstats
import os
import sys

try:
    import cProfile as profile
except ImportError:
    import profile

from flask import Blueprint, request, render_template, current_app


# Profile blueprint used to render template and serving static files
blueprint = Blueprint('_profile', __name__, static_folder='static',
                      static_url_path='/static', template_folder='templates',
                      url_prefix='/_profile')


def insensitive_replace(string, target, replacement):
    """string.replace() that is case insensitive.
    """
    no_case = string.lower()
    index = no_case.rfind(target.lower())
    if index >= 0:
        return string[:index] + replacement + string[index + len(target):]
    else:
        return string


def filename_format(filename):
    """Format the profiler filename.
    """
    if not os.path.isabs(filename):
        if filename.startswith(('{', '<')) or \
                filename.startswith('.' + os.path.sep):
            return filename
        return os.path.join('.', filename)

    if filename.startswith(current_app.root_path):
        return os.path.join('<approot>', filename[len(current_app.root_path):])

    prefix = ''
    prefix_len = 0
    for path in sys.path:
        current_prefix = os.path.commonprefix([path, filename])
        if len(current_prefix) > prefix_len:
            prefix = current_prefix
            prefix_len = len(prefix)
    filename = filename[prefix_len:]
    return os.path.join('<pylib>', filename)


class Profiler(object):
    """Profiler Extension.
    """

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """This is used to set up profiler for your flask app object.

        :param app: the Flask app object.
        """
        if app.debug:
            app.register_blueprint(blueprint)
            app.before_request(ProfilerTool.before_request)
            app.after_request(ProfilerTool.after_request)


class ProfilerTool(object):
    """Profiler.
    """

    def __init__(self):
        self.profiler = profile.Profile()
        self.stats = None
        self.profiler.enable()

    def disable(self):
        self.profiler.disable()
        self.stats = pstats.Stats(self.profiler)

    @property
    def func_calls(self):
        """Get collected profiling data.
        """
        func_calls = []
        if not self.stats:
            return func_calls

        for func in self.stats.sort_stats(1).fcn_list:
            info = self.stats.stats[func]
            stat = {}

            # Number of calls
            if info[0] != info[1]:
                stat['ncalls'] = "%d/%d" % (info[1], info[0])
            else:
                stat['ncalls'] = info[1]

            # Total time
            stat['tottime'] = info[2] * 1000

            # Time per call
            if info[1]:
                stat['percall'] = info[2] * 1000 / info[1]
            else:
                stat['percall'] = 0

            # Cumulative time spent in this and all subfunctions
            stat['cumtime'] = info[3] * 1000

            # Cumulative time per primitive call
            if info[0]:
                stat['percall_cum'] = info[3] * 1000 / info[0]
            else:
                stat['percall_cum'] = 0

            # Filename
            filename = pstats.func_std_string(func)
            stat['filename'] = filename_format(filename)

            func_calls.append(stat)

        return func_calls

    @property
    def total_time(self):
        if self.stats:
            return float(self.stats.total_tt) * 1000

    @property
    def content(self):
        """HTML content for your profile stats.
        """
        return render_template('_profile/profiler.html',
                               total_time=self.total_time,
                               func_calls=self.func_calls)

    @classmethod
    def before_request(cls):
        request._profiler_tool = ProfilerTool()

    @classmethod
    def after_request(cls, response):
        request._profiler_tool.disable()
        if response.status_code == 200 and \
                response.headers['content-type'].startswith('text/html'):
            html = response.data.decode(response.charset)
            html = insensitive_replace(
                html, '</body>', request._profiler_tool.content + '</body>')
            html = html.encode(response.charset)
            response.response = [html]
            response.content_length = len(html)
        return response
