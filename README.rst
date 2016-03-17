Flask-Profile
=============

A profiler extension for finding bottlenecks in Flask application.

Installation
------------

::

    $ pip install Flask-Profile

Usage
-----

.. code:: python
    
    from flask import Flask, render_template_string
    from flask.ext.profile import Profiler

    app = Flask(__name__)
    # Flask-Profile is only actived under debug mode
    app.debug = True
    Profiler(app)

    @app.route('/')
    def index():
        return render_template_string('<html><body>hello</body></html>')

    app.run()

You can also create the object once and configure the application later:

.. code:: python
    
    profiler = Profiler()

    def create_app():
        app = Flask(__name__)
        profiler.init_app(app)
        return app

If you want the profiler collects data including Extensions, please make sure
that the Extension is used after Flask-Profile:

.. code:: python
    
    from flask.ext.session import Session
    from flask.ext.profile import Profiler

    Profiler(app)
    Session(app)

.. note::
    
    You can click the column name to sort in the page.

Better
------

If you feel anything wrong, feedbacks or pull requests are welcome.
