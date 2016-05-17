"""
Flask-Profile
-------------

A profiler extension for finding bottlenecks in Flask application.

Links
`````

* `documentation <https://github.com/fengsp/flask-profile>`_
* `development version
  <http://github.com/fengsp/flask-profile/zipball/master#egg=Flask-Profile-dev>`_

"""
from setuptools import setup


setup(
    name='Flask-Profile',
    version='0.2',
    url='https://github.com/fengsp/flask-profile',
    license='BSD',
    author='Shipeng Feng',
    author_email='fsp261@gmail.com',
    description='Flask Application Profiler',
    long_description=__doc__,
    packages=['flask_profile'],
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=[
        'Flask >= 0.7'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
