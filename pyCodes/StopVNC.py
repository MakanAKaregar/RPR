#to stop VNC server
#useage example:
#to be added to the crontab to stop VNC after 300 seconds from boot
#@reboot sleep 300 && sudo /bin/python3.7 /home/pi/RPR/pyCodes/StopVNC.py

import os
os.system('sudo systemctl stop vncserver-x11-serviced.service')
