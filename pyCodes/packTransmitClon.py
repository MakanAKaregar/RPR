#to compress daily NMEA data and possibly transmit through secure copy (scp) to a data server
#useage example:
#to be added to the crontab to pack and trasfer compressed daily data at 12:10 AM to a remote server
#10 00 * * * /bin/python3.7 /home/pi/RPR/pyCodes/packTransmitClon.py

import os
import subprocess
from datetime import date
 
#get today's date
today = date.today()
yr = '{:02.0f}'.format(today.year) 
mn = '{:02.0f}'.format(today.month)
#get day of yesterday
dy = '{:02.0f}'.format(today.day-1)
#get the last two digits of year
yr = yr[2:4]

#dir of stored data in RPR
data_dir= '/home/pi/RPR/data/'

os.system('gzip '+data_dir+yr+mn+dy+'.log')
filename = data_dir+yr+mn+dy+'.log.gz'
subprocess.call(' scp ' + filename + ' remoteUserID@remoteIP:/remoteDirectory/')



