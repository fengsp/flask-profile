# -*- coding: utf-8 -*-
"""
    Simple Hello
    ~~~~~~~~~~~~

    Simple app to demo Flask-Profile.

    :copyright: (c) 2014 by Shipeng Feng.
    :license: BSD, see LICENSE for more details.
"""

from flask import Flask, render_template
from flask.ext.profile import Profiler


app = Flask(__name__)
app.debug = True
profiler = Profiler(app)


@app.route('/')
def index():
    return render_template('hello.html')


if __name__ == "__main__":
    app.run()
