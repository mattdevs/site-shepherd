#!/usr/bin/python
__author__ = 'mattdevs'

import logging
from flask import Flask
from flask import render_template

import shepherd_util

if __name__ == "__main__":
    """ Set up a basic web interface using Flask. """
    shepherd_util.setupLogging("shepherd_frontend.out")
    logging.info("Starting up web interface.")
    app = Flask(__name__)

    @app.route('/')
    def dashboard():
        siteList = shepherd_util.unpackSites()
        return render_template('dashboard.html', sites=siteList)

    app.run(debug=True)