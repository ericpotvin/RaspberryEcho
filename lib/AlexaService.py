# -*- coding: UTF-8 -*-
""" AlexaService: The Amazon Alexa service
"""

from lib import AUDIBLE_PATH
from lib.Config import Config
from lib.RecordVoice import RecordVoice

import json
import re
import requests
from os import system


class AlexaService(object):
    """ Alexa Module
    """

    # Amazon Settings
    AMAZON_BASE_URL = "https://www.amazon.com/ap/oa"
    AMAZON_TOKEN_URL = "https://api.amazon.com/auth/o2/token"
    AMAZON_SPEECH_URL = \
        "https://access-alexa-na.amazon.com/v1/avs/speechrecognizer/recognize"
    STATUS_OK = 200

    def __init__(self):
        pass

    @staticmethod
    def connected():
        """ Check if can connect to the Amazon oAuth2
            :return boolean
        """
        print "Checking Internet Connection"
        try:
            requests.get(AlexaService.AMAZON_TOKEN_URL)
            print "Connection OK"
            return True
        except requests.exceptions.Timeout as exception:
            print "Error: Timeout / " + exception.message
        except requests.exceptions.TooManyRedirects as exception:
            print "Error: Invalid URL provided / " + exception.message
        except requests.RequestException as exception:
            print "Error: Connection Failed / " + exception.message
            return False

    @staticmethod
    def get_token():
        """ Get the access token
            :return string
        """

        refresh_token = Config.get_config(Config.FIELD_REFRESH_TOKEN)

        if refresh_token:

            client_id = Config.get_config(Config.FIELD_CLIENT_ID)
            client_secret = Config.get_config(Config.FIELD_CLIENT_SECRET)

            auth_data = {
            "client_id": client_id,
            "client_secret": client_secret,
            "refresh_token": refresh_token,
            "grant_type": "refresh_token"
            }

            result = requests.post(
                AlexaService.AMAZON_TOKEN_URL,
                data=auth_data
            )
            resp = json.loads(result.text)
            Config.save_config(Config.FIELD_ACCESS_TOKEN, resp['refresh_token'])

            return resp['access_token']

        else:
            return False

    @staticmethod
    def send_request():
        """ Send the request
        """

        boundary = None
        audio = None

        headers = {'Authorization': 'Bearer %s' % AlexaService.get_token()}
        data = {
            "messageHeader": {
                "deviceContext": [
                    {
                        "name": "playbackState",
                        "namespace": "AudioPlayer",
                        "payload": {
                            "streamId": "",
                            "offsetInMilliseconds": "0",
                            "playerActivity": "IDLE"
                        }
                    }
                ]
            },
            "messageBody": {
                "profile": "alexa-close-talk",
                "locale": "en-us",
                "format": "audio/L16; rate=16000; channels=1"
            }
        }

        with open(AUDIBLE_PATH + RecordVoice.RECORD_FILE) as inf:
            files = [
                ('file',
                    ('request',
                     json.dumps(data),
                     'application/json; charset=UTF-8')),
                ('file',
                    ('audio',
                     inf,
                     'audio/L16; rate=16000; channels=1'))
            ]
            result = requests.post(
                AlexaService.AMAZON_SPEECH_URL,
                headers=headers,
                files=files
            )

        if not result.status_code == AlexaService.STATUS_OK:
            print "Error: Unable to send request (%s)" % result.status_code
            return

        for value in result.headers['content-type'].split(";"):
            if re.match(".*boundary.*", value):
                boundary = value.split("=")[1]

        data = result.content.split(boundary)

        for sound_data in data:
            if len(sound_data) >= 1024:
                audio = sound_data.split('\r\n\r\n')[1].rstrip('--')

        with open(AUDIBLE_PATH + RecordVoice.RESPONSE_FILE, 'wb') as audio_file:
            audio_file.write(audio)

        system(
            'mpg123 -q {}1sec.mp3 {}response.mp3 {}1sec.mp3' . format(
                AUDIBLE_PATH, AUDIBLE_PATH, AUDIBLE_PATH)
        )
