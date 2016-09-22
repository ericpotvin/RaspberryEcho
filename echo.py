# -*- coding: UTF-8 -*-
""" Main program
"""

from lib import BUTTON, AUDIBLE_PATH
from lib.AlexaService import AlexaService
from lib.RecordVoice import RecordVoice

import os
import RPi.GPIO as GPIO

if __name__ == "__main__":

    GPIO.setwarnings(False)
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    while not AlexaService.connected():
        print "."

    os.system('mpg123 -q {}1sec.mp3 {}hello.mp3' . format(
        AUDIBLE_PATH, AUDIBLE_PATH
    )
    )

    while True:
        # we wait for the button to be pressed
        GPIO.wait_for_edge(BUTTON, GPIO.FALLING)

        RecordVoice.record()

        AlexaService.send_request()
