#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from config.config import config
import sys
import logging

"""
This python file is responsible for running the web app.
"""

app = Flask(__name__)
conf = dict(SECRET_KEY=config['secret_key'],
            SQLALCHEMY_DATABASE_URI=config['sqlalchemy_database_uri'],
            GOOGLE_LOGIN_CLIENT_ID=config['google_login_client_id'],
            GOOGLE_LOGIN_CLIENT_SECRET=config['google_login_client_secret'],
            GOOGLE_LOGIN_REDIRECT_URI=config['google_login_redirect_uri'],
            SQLALCHEMY_TRACK_MODIFICATIONS=False)
app.config.update(conf)
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
if __name__ == '__main__':
    logging.basicConfig(filename=config['log_file'], level=logging.INFO)
    from routes.routes import *
    app.run(host="0.0.0.0", port=5000, debug=True)
