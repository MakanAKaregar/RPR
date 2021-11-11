# sudo pip3 install timezonefinder
# sudo pip3 install pytz
# sudo pip3 install pynmea2

import pynmea2
import io
import serial
import pytz
import logging
from timezonefinder import TimezoneFinder
import time
import sys
import os

logger = logging.getLogger()
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.DEBUG)

serial_port = '/dev/ttyACM0';# port for Adafruit Feather 32U4 board
baud_rate = 9600; # in your IDE code, that is Serial.begin(baud_rate)

ser_ls = serial.Serial(port = serial_port, baudrate = baud_rate, parity = serial.PARITY_NONE, stopbits = serial.STOPBITS_ONE, bytesize = serial.EIGHTBITS, timeout = 1) #listen to serial port 

sio = io.TextIOWrapper(io.BufferedRWPair(ser_ls, ser_ls))#buffered text stream

while True:
    try:
        ln = sio.readline() #read a (nmea) line from serial port
        NMEA = pynmea2.parse(ln)#parse nmea line

        if type(NMEA) == pynmea2.types.talker.RMC:

            status = NMEA.status

            if status == 'A':
                logger.debug('Got Fix')

                t = NMEA.datetime #date and time

                latitude = NMEA.latitude #lat of GPS rcvr
                longitude = NMEA.longitude #long of GPS rcvr

                tzf = TimezoneFinder()
                tZone_string = tzf.timezone_at(lng=longitude, lat=latitude)#find time zone for your GPS

                logger.debug('set timezone to %s', tZone_string)
                os.system(f"timedatectl set-timezone {Zone_string }")

                tZone = pytz.timezone(Zone_string)
                t_tZone = t.replace(tzinfo=pytz.utc).astimezone(tZone)

                logger.debug('Set time to %s', t_tZone)
                clk_id = time.CLOCK_REALTIME
                time.clock_settime(clk_id, float(time.mktime(t_tZone.timetuple())))

                break

    except serial.SerialException as e:
        logger.error('Device error: {}'.format(e))
        break
    except pynmea2.ParseError as e:

        logger.error('Parse error: {}'.format(e))
    except UnicodeDecodeError as e:
        logger.error('UnicodeDecodeError error: {}'.format(e))
    continue

