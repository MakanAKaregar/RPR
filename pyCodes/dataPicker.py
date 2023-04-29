## to read serial port and write its content into a .log file
## Note: The IDE sketch uploaded to GPS board is slightly modified in a way that it writes only GPS data to serial port and avoid extra texts
## Makan Karegar, Feb 6, 2020, Bonn. 

import serial#don't forget to install the serial package
from datetime import timezone
import datetime

file_path="/home/pi/RPR/data/"

date_now=str(datetime.datetime.now(timezone.utc)); #current date and UTC time

filename=(date_now[2:4]+date_now[5:7]+date_now[8:10]+'.log');# filename is set at the daily basis
output_file = open(file_path+filename,"a");#open output file

serial_port = '/dev/ttyACM0';# port for Adafruit Feather 32U4 board
baud_rate = 9600; # in your IDE code, that is Serial.begin(baud_rate)

ser_ls = serial.Serial(serial_port, baud_rate)#listen to serial port 

#getting the initialization date (UTC time)
date_ini = datetime.datetime.now(timezone.utc) 
RunDy = date_ini.day
RunMo = date_ini.month
RunYr = date_ini.year

while True:
    ln = ser_ls.readline();#read a line from serial port
    ln = ln.decode("utf-8") #convert binary to string
    print(ln);
    
    #getting the current date (UTC time)
    date_now = datetime.datetime.now(timezone.utc) + datetime.timedelta(seconds=18) 
    NowDy = date_now.day
    NowMo = date_now.month
    NowYr = date_now.year

    #check the current date with initialization date (as in RunDy, RunMo and RunYr)
    if (NowYr == RunYr and NowMo == RunMo and NowDy == RunDy):
        output_file.write(ln);
    else:
        date_now=str(datetime.datetime.now(timezone.utc));# current UTC date 
        filename=(date_now[2:4]+date_now[5:7]+date_now[8:10]+'.log');# filename is set at the daily basis
        output_file = open(file_path+filename,"a");
        print(ln);
        output_file.write(ln);
