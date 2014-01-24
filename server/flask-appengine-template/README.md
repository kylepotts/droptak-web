Flask on Google App Engine Template
======

A template for bootstrapping flask applications on google's app engine. It utilizes flask's excellent blueprints and comes with bootstrap 2.2, jinja2 and werkzeug.

Features:
-----

- Python 2.7 Runtime (Threadsafe)
- Flask (http://flask.pocoo.org/)
- Jinja2
- Werkzeug
- Testsuite
- Bootstrap

Quickstart:
-----


First, make sure you have virtualenv installed and that you are running python 2.7.

To get everything up and running clone/fork this repo and run:

    make setup

in the root directory. This will create a new virtual environment and fetch the required packages + google sdk.
All required packages in site-packages are symlinked into app/lib.    
Almost there! To test your application on the local development server, run:

    make server

Nagivate your browser to localhost:8080 and verify that everything is working as expected.

Deploy:
-----

In case you want to deploy your app, first change the application name in app.yaml, then run:

    make deploy

This will resolve the symlinks in app/lib/ and deploy to app engine.

Tests:
-----

To run tests, place tests modules in your blueprints and run:

    make tests


