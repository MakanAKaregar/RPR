#to power on USB dongle port (USB D socket)
# USB ports and LAN port in RP 3B+ are in the following order:
#LAN   A   D
#      B   C
#useage example:
#o be added to the crontab to power on USB dongle port at 12:05 AM
#05 00 * * * sudo /bin/python3.7 /home/pi/RPR/pyCodes/PowerOnUSBdongle.py

import os
os.system("cd /home/pi/RPR/hub-ctrl.c ; sudo ./hub-ctrl -h 1 -P 3 -p 1")
