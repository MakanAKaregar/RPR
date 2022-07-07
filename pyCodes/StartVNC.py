#to start VNC server
#useage example:
#to be added to the crontab to start VNC at reboot
#@reboot sudo /bin/python3.7 /home/pi/RPR/pyCodes/StartVNC.py

import os
os.system('sudo systemctl start vncserver-x11-serviced.service')

