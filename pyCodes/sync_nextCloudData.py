#add this code to crontab 
#*/1 * * * * /bin/python3.9 /home/pi/RPR/pyCodes/sync_nextCloudData.py

nextcloud_localDir = '/home/pi/RPR/data'#RPR’s NMEA data driectory
streaming_interval = 60 #streaming interval in second. Best to be equal to the interval given in your cron job 

from os import *
import time

system('touch  '+nextcloud_localDir+'/.dummy')

time.sleep(streaming_interval) 

system('rm  '+nextcloud_localDir+'/.dummy')
