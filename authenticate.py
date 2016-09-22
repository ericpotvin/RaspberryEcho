# -*- coding: UTF-8 -*-
""" Authenticate the user credentials
"""

from lib.AlexaService import AlexaService
from lib.Config import Config

import cherrypy
import os
import requests
import json
import urllib


class Start(object):
    """ The Web object
    """

    def index(self):
        """ The main page
        """

        product_id = Config.get_config(Config.FIELD_PRODUCT_ID)
        client_id = Config.get_config(Config.FIELD_CLIENT_ID)

        scope_data = json.dumps(
            {"alexa:all": {
            "productID": product_id,
            "productInstanceAttributes": {
                "deviceSerialNumber": "001"}
            }}
        )
        callback = cherrypy.url() + "code"

        payload = {
            "client_id": client_id,
            "scope": "alexa:all",
            "scope_data": scope_data,
            "response_type": "code",
            "redirect_uri": callback
        }
        req = requests.Request(
            'GET', AlexaService.AMAZON_BASE_URL, params=payload
        )
        raise cherrypy.HTTPRedirect(req.prepare().url)

    def code(self, var=None, **params):
        """ The code page
        """

        client_id = Config.get_config(Config.FIELD_CLIENT_ID)
        client_secret = Config.get_config(Config.FIELD_CLIENT_SECRET)

        code = urllib.quote(cherrypy.request.params['code'])
        callback = cherrypy.url()
        payload = {
            "client_id" : client_id,
            "client_secret" : client_secret,
            "code" : code,
            "grant_type" : "authorization_code",
            "redirect_uri" : callback
        }
        result = requests.post(AlexaService.AMAZON_TOKEN_URL, data=payload)
        result = result.json()

        # Save the refresh token and reset access token
        Config.save_config(
            Config.FIELD_REFRESH_TOKEN,
            format(result['refresh_token'])
        )
        Config.save_config(Config.FIELD_ACCESS_TOKEN, "")

        html = "<b>Success!</b><br/>"
        html += "Refresh token has been added to your credentials file.<br/>"
        html += "You may now reboot the Pi or restart the service.<br/>"
        html += "Your token: %s" % result['refresh_token']

        return html

    index.exposed = True
    code.exposed = True

if __name__ == "__main__":
    cherrypy.config.update(
        {'server.socket_host': '0.0.0.0'}
    )
    cherrypy.config.update(
        {'server.socket_port': int(os.environ.get('PORT', '5000'))}
    )
    cherrypy.quickstart(Start())
