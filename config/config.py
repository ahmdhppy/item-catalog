# -*- coding: utf-8 -*-
import optparse
import os
import ConfigParser


class configmanager(object):
    """
        Configuration Class which parses the config file
        data to be used in the web app.
    """

    def __init__(self):
        self.options = dict(
            db_name='itemcatalog',
            db_user='admin',
            db_password='admin',
            db_host='localhost',
            db_port=5432,
            secret_key='DEPLOYMENT SECRET KEY',
            google_login_client_id='GOOGLE LOGIN CLIENT ID',
            google_login_client_secret='GOOGLE LOGIN CLIENT SECRET',
            google_login_redirect_uri='oauth2callback',
            log_file='logfile.log')

        parser = optparse.OptionParser()
        parser.add_option('-c',
                          '--config',
                          dest="config",
                          help="specify config file")
        options, args = parser.parse_args()
        if options.config:
            if os.path.isfile(options.config):
                configParser = ConfigParser.RawConfigParser()
                configParser.read(options.config)
                for section in configParser.sections():
                    self.options.update(dict(configParser.items(section)))

            else:
                raise Exception(
                    '''The config file cannot be found
                     in the specifiedlocation,
                    please read instructions for assistance. (README.md).''')
        uri = 'postgresql://%(db_user)s:%(db_password)s'\
            '@%(db_host)s:%(db_port)s/%(db_name)s'
        self.options['sqlalchemy_database_uri'] = uri % self.options

    def __getitem__(self, key):
        return self.options.get(key, '')


config = configmanager()
