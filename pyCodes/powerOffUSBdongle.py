#to power off USB dongle port (USB D socket)
# USB ports and LAN port in RP 3B+ are in following order:
#LAN   A   D
#      B   C
#useage example:
#o be added to the crontab to power off USB dongle port 300 seconds after boot
@reboot sleep 300 && sudo /bin/python3.7 /home/pi/RPR/pyCodes/powerOffUSBdongle.py


import os
import time
os.system("sudo pkill -f dataPicker.py")#kill dataPicker.py
time.sleep(1)
os.system("cd /home/pi/RPR/hub-ctrl.c ; sudo ./hub-ctrl -h 1 -P 2 -p 0")#power off all usb
os.system("cd /home/pi/RPR/hub-ctrl.c ; sudo ./hub-ctrl -h 1 -P 2 -p 0")#power off all usb
time.sleep(2)
os.system("cd /home/pi/RPR/hub-ctrl.c ; sudo ./hub-ctrl -h 1 -P 2 -p 1")#power on all usb
time.sleep(2)
os.system("cd /home/pi/RPR/hub-ctrl.c ; sudo ./hub-ctrl -h 1 -P 3 -p 0")#power off usb D (dongle)
os.system("cd /home/pi/RPR/hub-ctrl.c ; sudo ./hub-ctrl -h 1 -P 3 -p 0")#power off usb D (dongle)

os.system("cd /home/pi/RPR/hub-ctrl.c ; sudo ./hub-ctrl -h 0 -P 2 -p 1")#power on usb A
time.sleep(2)
os.system("cd /home/pi/RPR/hub-ctrl.c ; sudo ./hub-ctrl -h 0 -P 2 -p 0")#power off usb A 
os.system("cd /home/pi/RPR/hub-ctrl.c ; sudo ./hub-ctrl -h 0 -P 2 -p 0")#power off usb A

os.system("cd /home/pi/RPR/hub-ctrl.c ; sudo ./hub-ctrl -h 0 -P 3 -p 1")#power on usb B
time.sleep(2)
os.system("cd /home/pi/RPR/hub-ctrl.c ; sudo ./hub-ctrl -h 0 -P 3 -p 0")#power off usb B 
os.system("cd /home/pi/RPR/hub-ctrl.c ; sudo ./hub-ctrl -h 0 -P 3 -p 0")#power off usb B

time.sleep(3)
os.system('/bin/python3.7 /home/pi/RPR/pyCodes/dataPicker.py')#run dataPicker.py



