"""
This converts RPR's nmea filename to a format compatible with gnssrefl software
Makan Karegar, Uni Bonn, Aug 30, 2021
"""

import argparse
import os
import sys
from datetime import datetime
from datetime import timedelta
    
Epilog = '''
setStaId.py converts RPR filename (YRMNDY.log.gz) to a file format compatible with gnssrefl software (SSSSdoy0.YR.A.gz)

Note: run setStaId.py for a single year.

-- Examples --
Example 1, Converting a single file
    python3.9 setStaId.py WESL 2021-01-01 /home/pi/RPR/data/

Example 2, Converting all files in 2021 
    python3.9 setStaId.py WESL 2021-01-01 /home/pi/RPR/data/ -date_end 2021-12-31

Example 3, Converting files from May 01, 2021 to July 15, 2021 
    python3.9 setStaId.py WESL 2021-05-01 /home/pi/RPR/data/ -date_end 2021-07-15
    
'''

parser=argparse.ArgumentParser(epilog=Epilog, formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument("station", help="desired station name (4 characters)", type=str)
parser.add_argument("date", help="date in YYYY-MM-DD format", type=str)
parser.add_argument("data_dir", help="data directory", type=str)
    
# optional arguments
parser.add_argument("-date_end", default=None, help="end date", type=str)

args = parser.parse_args()

station = args.station; 
NS = len(station)
if (NS != 4):
    print('Illegal input - Station name must have 4 characters. Exiting.')
    sys.exit()

date = args.date
if len(str(date)) != 10:
    print('Date must be ten characters long. Exiting.', date)
    sys.exit()    

if args.date_end == None:
    date2 = date
else:
    date2 = args.date_end
        
year1 = int(date[0:4])
mn1 = date[5:7]
day1 = date[8:10]
doy = datetime(int(year1),int(mn1),int(day1)).timetuple().tm_yday  # calculate doy of latency date

year2 = int(date2[0:4])
mn2 = date2[5:7]
day2 = date2[8:10]
doy2 = datetime(int(year1),int(mn2),int(day2)).timetuple().tm_yday  # calculate doy of latency date

doy_list = list(range(doy, doy2+1))
year_list = list(range(year1, year2+1))
    
data_dir = args.data_dir
                 
# loop over years and day of years
for year in year_list:
        
    for doy in doy_list:
        calender_date = datetime.strptime(str(year)+' ' + str(doy), '%Y %j')
        mn = calender_date.month
        day = calender_date.day
        yr =  '{:02d}'.format(year-2000)   
        filename = yr+'{:02d}'.format(mn)+'{:02d}'.format(day)+'.log' #e.g. 210930.log.gz
        
        today=datetime(year,12,31)
        doy31 = (today - datetime(year, 1, 1)).days + 1
        illegal_day = False
        if (float(doy) > doy31):
            illegal_day = True
        
        if (not illegal_day):
                
            if os.path.exists(data_dir+filename+'.gz'):
                    os.system('gunzip ' + data_dir + filename)
                    os.system('mv ' + data_dir + filename + ' ' + data_dir + station+'{:03d}'.format(doy)+'0.'+yr+'.A')
                    os.system('gzip ' + data_dir + station+'{:03d}'.format(doy)+'0.'+yr+'.A') 
                    print('setting RPR file '+yr + ' ' + '{:02d}'.format(mn) +' '+'{:02d}'.format(day))

            else:
                    print('RPR gzip file '+yr + ' ' + '{:02d}'.format(mn) +' '+'{:02d}'.format(day)+'  does not exist')
