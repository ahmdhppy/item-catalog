#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
from config.config import config
from app import db
from sqlalchemy_utils import database_exists, create_database
from models.models import *

import logging

"""
This python file creates the Database when run.
"""

if __name__ == '__main__':
    engine = db.create_engine(config['sqlalchemy_database_uri'])
    if not database_exists(engine.url):
        create_database(engine.url)
    else:
        logging.warning("A database with that name already exists.")
    db.create_all()
