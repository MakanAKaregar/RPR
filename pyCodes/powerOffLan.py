#to power off LAN port
#useage example:
#power off the LAN port after boot
#@reboot sudo /bin/python3.7 /home/pi/RPR/pyCodes/powerOffLan.py

import os
os.system("cd /home/pi/RPR/hub-ctrl.c-master ; sudo ./hub-ctrl -h 0 -P 1 -p 0")
os.system("cd /home/pi/RPR/hub-ctrl.c-master ; sudo ./hub-ctrl -h 0 -P 1 -p 0")


