## to read serial port and write its content into a .log file
## Note: The IDE sketch uploaded to GPS board is slightly modified in a way that it writes only GPS data to serial port and avoid extra texts
## Makan Karegar, Feb 6, 2020, Bonn. 

import serial# don't forget to install the serial package
import datetime

file_path="/home/pi/RPR/data/" # path for saving daily GPS SNR data

date_now=str(datetime.datetime.now());# current date and time

filename=(date_now[2:4]+date_now[5:7]+date_now[8:10]+'.log');# filename is set at the daily basis
output_file = open(file_path+filename,"w+");#open output file

serial_port = '/dev/ttyACM0';# port for Adafruit Feather 32U4 board
baud_rate = 9600; # in your IDE code, that is Serial.begin(baud_rate)

ser_ls = serial.Serial(serial_port, baud_rate)#listen to serial port 

while True:
    ln = ser_ls.readline();#read a line from serial port
    
    ln = ln.decode("utf-8") #convert binary to string

    if len(ln)==12 and ln[0:10]!=filename:#check if the first line is "filename.log" and differs to what you defined previously (line 11)
        filename=ln[0:10];#replace filename if differs from the one defined  
        output_file = open(file_path+filename,"w+");
        print(ln);
        output_file.write(ln);
    else:
    
        print(ln);
        output_file.write(ln);
     
