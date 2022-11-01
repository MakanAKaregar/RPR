#to compress daily NMEA data and possibly transmit through secure copy (scp) to a data server
#useage example:
#to be added to the crontab to pack and trasfer compressed daily data at 12:10 AM to a remote server
#10 00 * * * /bin/python3.7 /home/pi/RPR/pyCodes/packTransmitCron.py

import os
import subprocess
from datetime import date, timedelta
 
#today's date
today = date.today()

#day, month and year of yesterday
yesterday = today - timedelta(days=1)
dy = '{:02.0f}'.format(yesterday.day)
mn = '{:02.0f}'.format(yesterday.month)
yr = '{:02.0f}'.format(yesterday.year) 

#get the last two digits of year
yr = yr[2:4]

#dir of stored data in RPR
data_dir= '/home/pi/RPR/data/'

os.system('gzip '+data_dir+yr+mn+dy+'.log')
filename = data_dir+yr+mn+dy+'.log.gz'
subprocess.call(' scp ' + filename + ' remoteUserID@remoteIP:/remoteDirectory/')
