# -*- coding: utf-8 -*-
"""
    flaskext.profile
    ~~~~~~~~~~~~~~~~

    Adds profiling to Flask.

    :copyright: (c) 2014 by Shipeng Feng.
    :license: BSD, see LICENSE for more details.
"""

import profile


class Profiler(object):
    """Profiler.
    """
    
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """This is used to set up profiler for your flask app object.

        :param app: the Flask app object.
        """
        pass
