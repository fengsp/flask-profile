# -*- coding: utf-8 -*-
"""
    flaskext.profile
    ~~~~~~~~~~~~~~~~

    Adds profiling to Flask.

    :copyright: (c) 2014 by Shipeng Feng.
    :license: BSD, see LICENSE for more details.
"""

try:
    import cProfile as profile
except ImportError:
    import profile
import pstats

from flask import Blueprint, render_template


# Profile blueprint used to render template and serving static files
blueprint = Blueprint('_profile', __name__, static_folder='static',
                      static_url_path='static', template_folder='templates',
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


class Profiler(object):
    """Profiler.
    """
    
    def __init__(self, app=None):
        self.app = app
        self.profiler = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """This is used to set up profiler for your flask app object.

        :param app: the Flask app object.
        """
        if app.debug:
            app.register_blueprint(blueprint)
            app.before_request(self.before_request)
            app.after_request(self.after_request)

    @property
    def stats(self):
        """Get collected profiling data.
        """
        stats = pstats.Stats(self.profiler)
        func_calls = []
        for func in stats.sort_stats(1).fcn_list:
            info = stats.stats[func]
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
            stat['filename'] = filename

            func_calls.append(stat)

        return func_calls

    @property
    def content(self):
        """HTML content for your profile stats.
        """
        return render_template('profiler.html', stats=self.stats)

    def before_request(self):
        self.profiler = profile.Profile()
        self.profiler.enable()

    def after_request(self, response):
        self.profiler.disable()
        if response.status_code == 200 and \
                response.headers['content-type'].startswith('text/html'):
            html = response.data.decode(response.charset)
            html = insensitive_replace(html, '</body>', 
                                       self.content + '</body>')
            html = html.encode(response.charset)
            response.response = [html]
            response.content_length = len(html)
        return response
