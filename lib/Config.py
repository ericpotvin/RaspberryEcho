# -*- coding: UTF-8 -*-
""" Config File/settings
"""

import ConfigParser


class Config(object):
    """ Save the amazon Alexa's keys
    """

    CONFIG_FILE = "amazon.ini"
    MAIN_SECTION = "main"
    FIELD_PRODUCT_ID = "product_id"
    FIELD_CLIENT_ID = "client_id"
    FIELD_CLIENT_SECRET = "client_secret"
    FIELD_REFRESH_TOKEN = "refresh_token"
    FIELD_ACCESS_TOKEN = "access_token"

    def __init__(self):
        pass

    @staticmethod
    def save_config(key, token):
        """ Save a config key/value
            :param key: The key
            :param token: The value
        """
        config = ConfigParser.ConfigParser()
        config.read(Config.CONFIG_FILE)

        # update existing value
        config.set(Config.MAIN_SECTION, key, token)

        with open(Config.CONFIG_FILE, 'w') as configfile:
            config.write(configfile)

    @staticmethod
    def get_config(key):
        """ Get a config value
        :param key: The key
        :return: string
        """

        config = ConfigParser.ConfigParser()
        config.read(Config.CONFIG_FILE)

        try:
            val = config.get(Config.MAIN_SECTION, key)
        except ConfigParser.ParsingError as exception:
            print "Error: Cannot parse the config file for key: %s / %s!" %\
                  (key, exception.message)
            return ""
        except Exception as exception:
            print "Error: Invalid key %s, got %s!" % (key, exception.message)
            return ""

        return val
