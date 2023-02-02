#to power off HDMI ports
#useage example:
#to be added to the crontab to switch off the HDMI ports after 30 sec from boot
#@reboot sleep 30 && sudo /bin/python3.9 /home/pi/RPR/pyCodes/powerOffHdmi.py

import os
#os.system('sudo /opt/vc/bin/tvservice -o')
os.system('sudo /usr/bin/tvservice -o')

