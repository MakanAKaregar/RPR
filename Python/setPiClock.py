# sudo pip3 install timezonefinder
# sudo pip3 install pytz
# sudo pip3 install pynmea2

import pynmea2
import io
import serial
import time
import pytz
import logging
import sys
import os
from timezonefinder import TimezoneFinder

logger = logging.getLogger()
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.DEBUG)

ser = serial.Serial(
    port = '/dev/ttyACM0',
    baudrate = 9600,
    parity = serial.PARITY_NONE,
    stopbits = serial.STOPBITS_ONE,
    bytesize = serial.EIGHTBITS,
    timeout = 1
)
sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))

while True:
    try:
        line = sio.readline()
        msg = pynmea2.parse(line)

        if type(msg) == pynmea2.types.talker.RMC:

            status = msg.status

            if status == 'A':
                logger.debug('Got Fix')

                zeit = msg.datetime

                latitude = msg.latitude
                longitude = msg.longitude

                tf = TimezoneFinder()
                zeitzone_string = tf.timezone_at(lng=longitude, lat=latitude)

                logger.debug('Set timezone to %s', zeitzone_string)
                os.system(f"timedatectl set-timezone {zeitzone_string}")

                zeitzone = pytz.timezone(zeitzone_string)
                zeit_mit_zeitzone = zeit.replace(tzinfo=pytz.utc).astimezone(zeitzone)
                unix_zeit = time.mktime(zeit_mit_zeitzone.timetuple())

                logger.debug('Set time to %s', zeit_mit_zeitzone)
                clk_id = time.CLOCK_REALTIME
                time.clock_settime(clk_id, float(unix_zeit))

                break

    except serial.SerialException as e:
        logger.error('Device error: {}'.format(e))
        break
    except pynmea2.ParseError as e:

        logger.error('Parse error: {}'.format(e))
    except UnicodeDecodeError as e:
        logger.error('UnicodeDecodeError error: {}'.format(e))
    continue

