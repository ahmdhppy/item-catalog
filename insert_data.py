#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
import psycopg2
from config.config import config
"""
This python file creates the demo categories.
"""

con = psycopg2.connect(database=config['db_name'],
                       user=config['db_user'],
                       password=config['db_password'],
                       host=config['db_host'],
                       port=config['db_port'])

category_name = ['Soccer', 'baseball', 'Frisbee']
category_name = ["('%s')" % name for name in category_name]
value = ','.join(category_name)
sql = """INSERT INTO categories(name)
VALUES %s;""" % value
cursor = con.cursor()

cursor.execute(sql)
con.commit()
