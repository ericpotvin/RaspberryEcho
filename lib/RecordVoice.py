# -*- coding: UTF-8 -*-
""" Record voice
"""

from lib import BUTTON, DEVICE, AUDIBLE_PATH

import alsaaudio
import RPi.GPIO as GPIO


class RecordVoice(object):
    """ Record voice Module
    """

    RECORD_FILE = "recording.wav"
    RESPONSE_FILE = "response.mp3"

    def __init__(self):
        pass

    @staticmethod
    def record():
        """ Record voice
        """
        inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL, DEVICE)
        inp.setchannels(1)
        inp.setrate(16000)
        inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
        inp.setperiodsize(500)

        audio = ""
        # we keep recording while the button is pressed
        while GPIO.input(BUTTON) == 0:
            valid, data = inp.read()
            if valid:
                audio += data
        save_audio = open(AUDIBLE_PATH + RecordVoice.RECORD_FILE, 'w')
        save_audio.write(audio)
        save_audio.close()
