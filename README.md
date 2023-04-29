## Key Points 
* The Raspberry Pi Reflector (RPR) is a prototype for tracking water levels with centimeter level accuracy
* RPR consists of cost-effective single-frequency Global Positioning System module and navigation antenna connected to  
  Raspberry Pi microcomputer
* RPR uses Interferometric Reflectometry technique and can be operated safely in extreme weather with lower operational costs

For more information about the RPR sensor, please check out our paper:

Karegar, M.A., Kusche, J., Nievinski, F.G., Larson, K.M. (2022). Raspberry Pi Reflector (RPR): a Low-cost Water-level Monitoring System based on GNSS Interferometric Reflectometry, Water Resources Research (in press), https://doi.org/10.1029/2021WR031713 

<p align=center>
<img src="https://github.com/MakanAKaregar/RPR/blob/main/Figure2.png" width="600"/>
</p>
The RPR hardware array comprising: (a) Raspberry Pi 4 Model B (b) Adafruit Feather Adalogger microcontroller (c) Adafruit GPS FeatherWing receiver (d) GPS external antenna (e) Configuration of RPR prototype setup used. This setup uses 4G/LTE dongle modem. 

### Table of Contents

1. [Installation guide for RPR](#RPRInst)
2. [Photovoltaic energy system for RPR](#solarPanel) 
3. [Installing nextCloud on RPR](#nextCloud) 

# 1. Installation guide for RPR (Raspberry Pi Reflector) <a name="RPRInst"></a> 


## 1.1 Raspberry Pi operating system installation 

   Raspberry Pi (RPi) does not have internal disk and built-in Operating System (OS). To set up RPi, an operating system needs to be installed onto a micro SD card. OS Image file is available at the official RPi website. The user needs to download and install RPi Imager to a computer with a micro SD card reader. Installation instruction can be found here: https://www.raspberrypi.com/software/ 

   After installing the OS onto the micro SD card, insert the card into the micro SD card slot of RPi. Peripheral devices such as monitor, keyboard and mouse are needed for initializing RPi. An HDMI/VGA monitor can be directly connected to RPi 3 using using a standard HDMI cable. For RPi 4, a micro HDMI to HDMI cable or a standard HDMI to HDMI cable along with a micro HDMI to HDMI adapter are needed. For a VGA monitor, use the HDMI to VGA adapter. Plug in monitor, USB keyboard and USB mouse to RPi. Plug in micro USB (RPi 3) or USB-C (RPi 4) power supply and connect to power.

   Once the RPi boots, open RPi Configuration under Applications Menu > Preferences > RPi Configuration. In the “Interfaces” tab, set SSH, VNC, Serial Port, Serial Console to enabled. Secure Shell (SSH) is a commonly used protocol for providing a secure channel between two computers. We can use SSH to connect from a Linux computer or from the Mac terminal to the RPi, without installing additional software. The [Virtual Network Connection (VNC) server](https://www.realvnc.com/en/blog/how-to-setup-vnc-connect-raspberry-pi/) is enabled for viewing GUI desktop of RPi remotely via VNC viewer software installed on a server computer. The GPS module sends and receives NMEA data via the serial communication port to the RPi. 

   After setting up the RPi, make sure that it has access to the internet.

## 1.2 Installing Arduino integrated development environment (IDE)
  
   1.2.1 Download the latest version of Arduino IDE (1.8.19) from Arduino website. Note that the processor of RPi 3 (4) is a 32- (64)- bit, 700 MHz system on a chip, which is built on the ARM11 architecture, thus we recommend installing “Linux ARM 32 bits” download option: https://www.arduino.cc/en/software
  
   1.2.2 Uncompress downloaded file:
   
   <code>tar -xf arduino-1.8.19-linuxarm.tar.xz</code>
  
   1.2.3 Change your current directory to the created folder and install the Arduino IDE using: 
  
   <code>cd  arduino-1.8.19</code>
   
   <code>sudo ./install.sh</code>
      
 ## 1.3 Assembling GPS module (MPHW) and connecting to the Raspberry Pi:
 
 General instructions for soldering Adafruit GPS FeatherWing, Adafruit Feather Adalogger microcontroller and stackable header can be found here (follow Section 2.1 in [Tutorial Adafruit GNSS-R.pdf](https://github.com/fgnievinski/mphw/blob/main/docs/Tutorial%20MPHW%20GNSS-R.pdf)):


Plug the assembled GPS (MPHW) module into RPi’s USB socket using a USB to Micro USB cable. 

## 1.4 Downloading Arduino and python codes:
  
1.4.1  Installing <code>git</code> 
 
 <code>sudo apt install git</code>
  
1.4.2  Change your current directory to:
  
  <code>cd /home/pi</code>
  
1.4.3 Download Arduino and python codes from GitHub using git commad:

  <code>git clone https://github.com/MakanAKaregar/RPR.git</code>
  
A new directory (RPR) is created under <code>/home/pi</code>  
    
1.4.4 Create a new directory for archiving RPR’s daily NMEA data:
    
<code>mkdir /home/pi/RPR/data</code>


## 1.5 Adding and installing Adafruit board support package for Arduino IDE

To enable the Arduino IDE to communicate with Adafruit Feather 32u4 Adalogger board we will need to install a board support package that includes Adafruit FeatherWing driver that allows us to upload Arduino sketch via the Arduino IDE. 

1.5.1 Start the IDE and navigate to File > Preference. Under “Settings” tab add the following URL in “Additional Boards Manager URLs”
https://adafruit.github.io/arduino-board-index/package_adafruit_index.json

1.5.2 Install Adafruit FeatherWing board

Tools > Board > Boards Manager > Contributed. Select “Adafruit AVR Boards” and click “Install” button.

1.5.3 Quit and reopen the Arduino IDE. Under Tools > Board, select “Adafruit Feather 32u4”

1.5.4 Under Tools > Port, select <code>/dev/ttyACM0</code>

1.5.5 Compile and upload the Arduino sketch:

- Open MPHW.ino sketch available from <code>/home/pi/RPR/ideCodes/</code> in the Arduino IDE: File > Open
- ensure that board and port are correct
- compile and upload the MPHW.ino to the Adafruit Feather 32u4 board under Sketch > Upload 

##### Note: if you use the new chipset (MTK3333) instead of legacy MTK3339-based module, you should change the default <code>GPS_BAUD_RATE</code> from <code>115200</code> to <code>9600</code> in MPHW.ino code.

1.5.6 Test GPS NMEA data streaming/transmitting to the serial port on terminal

Put the GPS antenna near or outside a window to get satellite signals. You can test if RPR setup is done correctly by the following command:

<code>cat /dev/ttyACM0</code>

This should give you results resembling the following outputs in your terminal:
```
$GPGGA,171540.000,5043.6373,N,00705.2537,E,1,09,0.85,63.6,M,47.7,M,,*5B
$GPGSV,4,1,13,24,77,293,26,19,41,093,39,15,41,182,15,12,38,224,29*70
$GPGSV,4,2,13,17,34,059,41,37,30,161,,13,23,151,29,10,23,295,16*70
$GPGSV,4,3,13,23,20,259,22,14,11,055,32,25,07,233,18,01,05,020,27*7D
$GPGSV,4,4,13,32,05,320,18*47
$GPRMC,171540.000,A,5043.6373,N,00705.2537,E,0.04,2.26,151121,,,A*6F
$GPRMC,171540.000,A,5043.6373,N,00705.2537,E,0.04,2.26,151121,,,A*6F
211115.log
```
```
$GPGGA,171541.000,5043.6373,N,00705.2540,E,1,09,0.88,63.6,M,47.7,M,,*57
$GPGSV,4,1,13,24,77,293,26,19,41,093,39,15,41,182,16,12,38,224,29*73
$GPGSV,4,2,13,17,34,059,41,37,30,161,,13,23,151,28,10,23,295,16*71
$GPGSV,4,3,13,23,20,259,22,14,11,055,32,25,07,233,18,01,05,020,27*7D
$GPGSV,4,4,13,32,05,320,18*47
$GPRMC,171541.000,A,5043.6373,N,00705.2540,E,0.02,25.95,151121,,,A*55
$GPRMC,171541.000,A,5043.6373,N,00705.2540,E,0.02,25.95,151121,,,A*55
211115.log
```

## 1.6 Updating GPS module’s firmware (only applicable to legacy MTK3339-based module)

To generate the SNR data with 0.1-dB precision we should update Adafruit GPS FeatherWing’s firmware. To perform the firmware update, we require a Windows computer to install The GlobalTop Flash Tool software which allows updating the firmware of GPS chip. The custom firmware for the MediaTek GPS can be made available upon request. After updating the GPS firmware, plug the GPS module into the RPi and redo steps from 5.3 to 5.6.
You can test if the GPS firmware is upgraded by the following command:

<code>cat /dev/ttyACM0</code>

This should give you the following sentences in your terminal:

```
$GPGGA,172644.000,5043.6391,N,00705.2406,E,1,5,1.50,66.1,M,47.7,M,,*67
$GPGSV,2,1,06,24,82,295,26.2,12,44,227,32.4,19,42,087,44.2,17,32,054,42.4*7E
$GPGSV,2,2,06,13,18,152,34.6,23,17,255,24.6*76
$GPRMC,172644.000,A,5043.6391,N,00705.2406,E,0.14,290.38,151121,,,A*63
$GPRMC,172644.000,A,5043.6391,N,00705.2406,E,0.14,290.38,151121,,,A*63
211115.log</code>
```

```
$GPGGA,172645.000,5043.6391,N,00705.2406,E,1,5,1.50,65.9,M,47.7,M,,*6D
$GPGSV,2,1,06,24,82,295,25.0,12,44,227,32.3,19,42,087,44.4,17,32,054,42.0*7A
$GPGSV,2,2,06,13,18,152,34.4,23,17,255,25.2*71
$GPRMC,172645.000,A,5043.6391,N,00705.2406,E,0.14,290.38,151121,,,A*62
$GPRMC,172645.000,A,5043.6391,N,00705.2406,E,0.14,290.38,151121,,,A*62
211115.log
```

Note: if you use the new chipset (MTK3333) instead of legacy MTK3339-based module:
MTK3333 does not support the output of non-integer SNR values. You can skip step 1.6 if you use MTK3333. 

## 1.7 Installing some python packages and sshpass utility:

Make sure your RPi is connected to the internet. We will need a few additional python packages to make the python scripts work. Running the following command from terminal will install these libraries:

1.7.1  <code>sudo apt-get update</code>

1.7.2  <code>sudo pip3 install pyserial</code>

1.7.3  <code>sudo pip3 install timezonefinder</code>

1.7.4  <code>sudo pip3 install pytz</code>

1.7.5  <code>sudo pip3 install pynmea2</code>

1.7.6  Install non-interactive <code>ssh</code> password provider <code>sshpass</code>

       
## 1.8  Setting systemd for service configuration to collect data at startup on RPR       

 1.8.1 Change your current directory to:
 
  <code>cd /lib/systemd/system/</code>

 1.8.2 Create a service unit file called <code>dataPicker.service</code>. systemd uses the python code <code>dataPicker.py</code> to run at startup on RPR
 
  <code>sudo nano dataPicker.service</code>
 
 1.8.3 Paste the following lines to your <code>dataPicker.service</code> 
  
```
[Unit]
Description=RPR data picking
After=After=network.target

[Service]
Type=simple
ExecStart=/bin/python3.9 /home/pi/RPR/pyCodes/dataPicker.py
Restart=always

[Install]
WantedBy=multi-user.target

```

and save the <code>dataPicker.service</code> file by pressing <Ctrl> + x followed by y and then press <Enter>.

1.8.3 Change the permission on the <code>dataPicker.service</code> file:
  
  <code>sudo chmod 644 /lib/systemd/system/dataPicker.service</code>

1.8.4 Set the execute permission on <code>dataPicker.py</code> file, allowing it to be run as a program:
  
  <code>chmod +x /home/pi/RPR/pyCodes/dataPicker.py</code>

1.8.5 Reload systemd files. This ensures running possible changed unit files in <code>dataPicker.service</code>:
  
  <code>sudo systemctl daemon-reload</code>
  
1.8.6 Enable the service to run automatically every time RPR boots up:
  
  <code>sudo systemctl enable dataPicker.service</code>

1.8.7 You can now start the service to manually verify collecting data:
  
  <code>sudo systemctl start dataPicker.service</code>


## 1.8 Setting crontab jobs

We automate data picking and RPi’s clock synchronization by setting up two boot-based cron jobs that run python codes whenever the RPi boots up. To create a crontab file, execute the following commands in a terminal:

1.8.1 <code>crontab -e</code>

You can select a text editor to make changes to the crontab file. Select your desired text editor (e.g. nano, vi ...).

1.8.2 Add these lines to the crontab file: 

<code>#to parse RPR nmea data into daily files after 60 sec from boot</code>

<code>@reboot sleep 60 && /bin/python3.7 /home/pi/RPR/pyCodes/dataPicker.py</code>

<code>#to synchronize Raspberry Pi’s clock with GPS time (it is local time) after 65 sec from boot</code>

<code>@reboot sleep 65 && sudo /bin/python3.7 /home/pi/RPR/pyCodes/setPiClock.py</code>

Note that for RPi 3 B and B+ the python source code is at <code>/bin/python3.7</code> and for RPi 4 at <code>/usr/bin/python3.7</code>

A simple code can be added to the time-based cronjob scheduler for compressing daily NMEA files and transfer to a server. For example, the python code packTransmitCron.py will be run every day at 12:10 AM:

<code>#to compress daily RPR files and transfer to a remote server at 12:10 AM</code>

<code>10 00 * * * /bin/python3.7 /home/pi/RPR/pyCodes/packTransmitCron.py</code>


Ensure that you included the correct file path in your crontab command. 

1.8.4 Example of cronjob schedules for a RPR powering with photovoltaic energy system.

This setting uses a USB dongle for transmitting daily pack of NMEA data (not a real-time streaming).

This block powers off the LAN and HDMI ports to save energy when RPR reboots. Then it runs VNC service and USB dongle for 5 minutes for any remote maintenance. 

<code>##--------------power management--------------</code>

<code>#power off the LAN port after boot</code>

<code>@reboot sudo /bin/python3.7 /home/pi/RPR/pyCodes/powerOffLan.py</code>

<code>#switch off the HDMI port after boot</code>

<code>@reboot /bin/python3.7 /home/pi/RPR/pyCodes/powerOffHdmi.py</code>

<code>#start VNC server after reboot</code>

<code>@reboot sudo /bin/python3.7 /home/pi/RPR/pyCodes/StartVNC.py</code>

<code>#power off USB dongle 300 seconds after boot</code>

<code>@reboot sleep 300 && sudo /bin/python3.7 /home/pi/RPR/pyCodes/powerOffUSBdongle.py</code>

<code>#stop VNC server 300 seconds after reboot</code>

<code>@reboot sleep 300 && sudo /bin/python3.7 /home/pi/RPR/pyCodes/StopVNC.py</code>

This block initiates data collection 60 seconds after RPR boots and synchronizes the RPR clock using GPS data.

<code>##--------------data collection--------------</code>

<code>#to parse RPR nmea data into daily files after 60 sec from boot</code>

<code>@reboot sleep 60 && /bin/python3.7 /home/pi/RPR/pyCodes/dataPicker.py </code>

<code>#to synchronize Raspberry Pi’s clock with GPS time after 65 sec from boot</code>

<code>@reboot sleep 65 && sudo /bin/python3.7 /home/pi/RPR/pyCodes/setPiClock.py</code>

This block powers on USB dongle (at 12:05 AM), compresses and transmits daily NMEA data to a remote data server (at 12:10 AM) and then powers off USB dongle (at 12:15 AM).

<code>##--------------data packing and transmit--------------</code>

<code>#power on USB dongle at 12:05 AM</code>

<code>05 00 * * * sudo /bin/python3.7 /home/pi/RPR/pyCodes/powerOnUSBdongle.py</code>

<code>#compress daily RPR file and transfer to a remote server at 12:10 AM</code>

<code>10 00 * * * /bin/python3.7 /home/pi/RPR/pyCodes/packTransmitCron.py</code>

<code>#power off USB dongle at 12:15 AM</code>

<code>15 00 * * * sudo /bin/python3.7 /home/pi/RPR/pyCodes/powerOffUSBdongle.py</code>

A cron task outputs its logs to <code>/var/log/syslog</code>. To turn on this capability, open <code>rsyslog.conf</code> using nano:

<code>sudo nano /etc/rsyslog.conf</code>

and Press <Ctrl> + w to search for <code>cron</code> in the opened file, then uncomment <code>cron.*</code>.

# 2. Photovoltaic energy system for the RPR<a name="solarPanel"></a> 

We measured the RPR’s power consumption using a USB multimeter providing current (A) and Voltage (V) in real time. The power usage will be W (Watt) = A (Ampere) * V (Voltage). We minimized the power consumption of Raspberry Pi (RPi) microcomputer by disabling HDMI output, LEDs, WI-FI & Bluetooth and LAN ports (see instruction here: https://learn.pi-supply.com/make/how-to-save-power-on-your-raspberry-pi/). We measured the power consumption of RPi 3B+ and 4B on idle state. The power constitutions for RPi 3B+ and 4B are about 0.7 W and 1.6 W, respectively. We thus recommend using RPi 3B+ with 1GB RAM instead of RPi 4B when supplying power with photovoltaic energy system. To disable the power of each USB port on the RPi 3B+, we use hub-ctrl.c code available at https://github.com/codazoda/hub-ctrl.c. 

To download and compile <code>hub-ctrl.c</code>, run the following command from RPi’s terminal:

<code>mkdir /home/pi/RPR</code>

<code> cd /home/pi/RPR/</code>

<code>sudo apt-get update</code>

<code>sudo apt-get install git gcc libusb-dev</code>

<code>git clone https://github.com/codazoda/hub-ctrl.c</code>

<code> cd hub-ctrl.c/</code> 

<code>gcc -o hub-ctrl hub-ctrl.c -lusb</code>

We have provided additional codes in the RPR repository that allow power control on the RPi 3 (https://github.com/MakanAKaregar/RPR/tree/main/pyCodes). These codes, for example, can be run as cron jobs when the RPR reboots. 

The total power consumption of a RPR with RPi 3B+ in idle mode is 0.7 W (0.14 A * 5 V). When the GPS data is collected the energy consumption reaches up to 1.0 W. Among RPR’s components, our GSM USB dongle (HUAWEI E3372) is energy-hungry and uses the highest amount of power. The RPR power consumption reaches up to about 2.5 W when the USB dongle is active and it drops to around 1.8 W when the USB dongle port is set off using hub-ctrl code.   

We have tested a RPR unit based on RPi 3B+ for two months in Bonn (Germany) following the Photovoltaic energy system shown in the Figure below and detailed in the Table. We measured the RPR’s power consumption while collecting GPS data, powering on the GSM dongle and streaming real-time data to a cloud. The RPR’s energy consumption stands at around 2.5 W, so the daily power consumption is around 60 Wh/day (2.5 W * 24 h). We used a 12V, 26 Ah lead-acid battery to power on the RPR. In theory, the battery can provide 312 Wh energy that would be sufficient for powering the RPR for around five days with no sunlight. When packing and sending daily GPS data is preferred, the dongle can be set to sleep mode and works based on a wake-up schedule to save power. In this case, the power consumption of RPR drops to 1.8 W and 43.2 Wh/day. Using hub-ctrl.c we provide a code that can be used in cron job for controlling USB dongle’s power
(https://github.com/MakanAKaregar/RPR/tree/main/pyCodes) (see Section 1.8.2).    

<p align=center>
<img src="https://github.com/MakanAKaregar/RPR/blob/main/Figure%20S3.jpg" width="600"/>
</p>

| component | function  | version | example source  |
| --- | --- | --- | --- |
| solar Panel | supplies input voltage to DC system | Sun Plus 80: 80W power 22.3V open circuit voltage | https://de.rs-online.com/web/p/solarpanels/1881233 |
| battery | *maintenance-free cycle sealed lead acid battery. *suitable for slow charge/discharge situations. *performs well in a broad temperature range. | MP26-12C: 12V, 26Ah | https://www.jewo.de/index.php/produkte/multipower/zyklentypen/item/93-mp26-12c |
| solar charger controller | *prevents the battery from overcharging/overdischarging *prevents a short-circuit between solar panel & battery *final charging voltage 14.1v *overdischarge disconnection 11.1v *activation voltage 12.4v |  12/24V; 6/6A | https://www.conrad.de/de/p/18310-laderegler-pwm-12-v-24-v-6-a-111182.html |
| power buck module | *provides USB port, DC plug & terminals *converts 12/24V to 5.2V; 5A | JZK 24v/12V to 5V; 5A | https://www.amazon.de/-/en/Power-Module-DC-DC-Supply-Converter/dp/B071ZRXKJY |
| Solar module cable | *connects solar panel to solar charger controller | QuickCab4 | https://order.phaesun.com/index.php/module-cable-phaesun-quickcab4-2-5-5.html |
| USB to micro USB plug cable | connects power buck module to RPi’s power microUSB socket | - | - |
| Strand cable | connects positive terminals of battery and power buck module to solar charger controller | 1.50 mm², red 1m | https://www.conrad.de/de/p/lapp-4520041-1-litze-h07v-k-1-x-1-50-mm-rot-1-m-607662.html | 
| Strand cable | connects positive terminals of battery and power buck module to solar charger controller | 1.50 mm², black, 1m | https://www.reichelt.de/ | 

# 3. Installing nextCloud on the RPR <a name="nextCloud"></a>

When streaming of NMEA data is preferred for real-time applications, the nextCloud and other client-server software can be installed on the RPR.

#### A) Install nextCloud server:

3.1 Update your package repositories and install <code>apache</code> web server software.

<code>sudo apt update</code>

<code>sudo apt upgrade</code>

<code>sudo apt-get install apache2</code>

To make sure apache is working on the RPR, open a web browser and enter your RPR’s IP to the URL bar.

3.2 Install <code>php</code> server scripting language and relevant packages.

<code>sudo apt install php8.0 php8.0-zip php8.0-sqlite3 php8.0-xml php8.0-imap php8.0-mbstring php8.0-curl php8.0-intl php8.0-gd php8.0-bz2 php-smbclient php8.0-gmp php8.0-mysql libapache2-mod-php8.0</code>

3.3 Make sure <code>mysql-common</code>  and  <code>mariadb-server</code> databases are already installed, if not do it so.
  
<code>sudo apt install mysql-common </code>
  
<code>sudo apt install mariadb-server</code>

3.4 Restart <code>apache</code>.
  
<code>sudo service apache2 restart</code>

3.5 Open <code>mysql</code> command-line client by assigning a password.
  
<code>sudo mysql -u root -p</code>

<code>Enter password:</code>

3.6 nextCloud requires a database for storing administrative data. Create nextclouddb database.
  
<code>CREATE DATABASE nextclouddb;</code> 
  
If nextclouddb database already exists, use <code>DROP DATABASE nextclouddb;</code> to delete it.

3.7 Create a user for the database. nextCloud uses this user to authenticate a connection with <code>mysql</code>.

<code>CREATE USER 'RPR'@'localhost' IDENTIFIED BY 'password';</code> 

Here we choose an arbitrary user called RPR and a password. If the user already exists, use <code>DROP USER 'RPR'@'localhost';</code> to delete it.

3.8 Grant permission of created database to the user database, then activate the granted permission for the user by flushing the privilege, and exit from <code>mysql</code> command-line client.

<code>GRANT ALL PRIVILEGES ON nextclouddb.* TO 'RPR'@'localhost';</code>
  
<code>FLUSH PRIVILEGES;</code>
  
You can quit the prompt by entering:
  
<code>quit;</code>

3.9 Change the current directory to:

<code>cd /var/www/</code>

3.10 Fetch the latest version of nextCloud from:

<code>sudo wget https://download.nextcloud.com/server/releases/latest.tar.bz2</code>

3.11 Extract files:

<code>sudo tar -xvf latest.tar.bz2</code>

3.12 Make a data directory for nextCloud.

<code>sudo mkdir -p /var/www/nextcloud/data</code>

3.13 Access <code>apache’s www-data</code> group to nextCloud and its data directory.

<code>sudo chown -R www-data:www-data /var/www/nextcloud/</code>

<code>sudo chmod 750 /var/www/nextcloud/data</code>

3.14 Configure apache web server for nextCloud by making an empty single file called <code> nextcloud.conf</code> .
  
<code>sudo nano /etc/apache2/sites-available/nextcloud.conf</code>
  
and then put the following in your <code>nextcloud.conf</code> 
```
Alias /nextcloud "/var/www/nextcloud/"

<Directory /var/www/nextcloud/>
  Require all granted
  AllowOverride All
  Options FollowSymLinks MultiViews

  <IfModule mod_dav.c>
    Dav off
  </IfModule>

</Directory>
```
3.15 Now enable <code>apache</code>’s configuration for nextCloud.

<code>sudo a2ensite nextcloud.conf</code>
  
3.16 Restart <code>apache</code> web server by using <code>systemctl</code> command to read updated configuration file.

<code>sudo systemctl reload apache2</code>

3.17 Modify <code>php</code> configuration file <code>php.ini</code> in order to increase the file upload size. By default, <code>php</code> file upload size is set to maximum 2 MB file on the server. Open <code>php</code> configuration file using nano.

<code>sudo nano /etc/php/8.0/apache2/php.ini</code>

and modify <code>post_max_size</code> and <code>upload_max_filesize</code> variables (Press <Ctrl> + w to search for text in nano):
  
<code>post_max_size = 2G</code>
  
<code>upload_max_filesize = 2G</code>

and save the <code>modified php.ini</code> file by pressing <Ctrl> + x followed by y and then press <Enter>. Then restart apache web server to read the updated configuration file.

<code>sudo service apache2 restart</code>

3.18 Enable HTTPS protocol with apache by configuring a SSL (Secure Sockets Layer) certificate. The SSL certificate is to encrypt a site's information and creates a more secure connection. Create a new directory to store the server key and certificate.

<code>sudo mkdir -p /etc/apache2/ssl</code>

Since there is no (free) certificate available from an external certification authority, we have to use SSL self-signed certificate in our local computer (the RPR microcomputer). Create a SSL certificate file apache.crt and a server key file apache.key protecting SSL certificate file, and place both files in the new directory created above.

<code>sudo openssl req -x509 -nodes -days 365 -newkey rsa:4096 -keyout /etc/apache2/ssl/apache.key -out /etc/apache2/ssl/apache.crt</code>

Here we can specify how long the SSL certificate remains valid by changing the default 365 days (<code>-days 365</code>) to an arbitrary number of days.

Now enable apache module mod_ssl that provides support for SSL encryption.

<code>sudo a2enmod ssl</code>

3.19 Set up the new certificate by modifying the SSL configuration file <code>default-ssl.conf</code>: 

<code>sudo nano /etc/apache2/sites-available/default-ssl.conf</code>

Change value of <code>DocumentRoot</code> variable to <code>/var/www/html/nextcloud</code>
  
Change value of <code>SSLCertificateFile</code> variable to <code>/etc/apache2/ssl/apache.crt</code>
  
Change value of <code>SSLCertificateKeyFile</code> variable to <code>/etc/apache2/ssl/apache.key</code>

and save the modified <code>default-ssl.conf</code> file.

3.20 Again enable <code>apache</code>’s configuration for new changes made and restart it.
  
<code>sudo a2ensite default-ssl.conf</code>

<code>sudo service apache2 restart</code>

3.21 To redirect the HTTP requests to HTTPS and enforce SSL usage on nextCloud (via HTTPS), open <code>000-default.conf</code> file.

<code>sudo nano /etc/apache2/sites-available/000-default.conf</code>

and add the following lines:
  
<code>RewriteEngine On</code>
  
<code>RewriteCond %{HTTPS} off</code>
  
<code>RewriteRule ^(.*)$ https://%{HTTP_HOST}$1 [R=301,L]</code>
  
and save the modified <code>000-default.conf</code> file.

3.22 Enable apache’s rewrite module <code>mod_rewrite</code> to invoke rewrite rules using:
  
<code>sudo a2enmod rewrite</code>
  
and then restart it
  
<code>sudo service apache2 restart</code>

and reboot the RPR:
  
<code>sudo reboot</code>

After RPR boots up, open nextCloud in the RPR's browser and enter your RPR’s IP to the URL bar followed by nextcloud as: https://YourRPR_IP/nextcloud. Since we do not have a signed key, click on Advanced and then Proceed to yourIP. 

Now create a Username and Password for your admin account. After clicking on Storage & database, select MySQL/MariaDB and provide the following database information you set in steps 3.6 and 3.7:

Database user >>  <code>RPR</code>
  
Database password >>  <code>passwordYouSetInStep7</code>
  
Database name >>  <code>nextclouddb</code>
  
In Data folder, add <code>/var/www/nextcloud/data</code> (see step 12).

Now the nextCloud server with its web interface is configured.

#### B) Install nextCloud desktop client:
  
The nextCloud desktop client provides the ability to place files in local directories, e.g., RPR’s daily NMEA data driectory (<code>/home/pi/RPR/data</code>), and synchronize them with the nextCloud server. The nextCloud desktop client nextcloud-desktop is not available yet (as of July 2022) in the RPi apt repository. However, it is available in the Debian repository http://ftp.debian.org/debian/.

Fetch a current archived key:
  
<code>wget https://ftp-master.debian.org/keys/archive-key-11.asc</code>
  
Use key management utility <code>apt-key</code> to add the downloaded key to the list of trusted keys.
  
<code>sudo apt-key add archive-key-11.asc</code>
  
Create a new file <code>debian.list</code> in folder <code>/etc/apt/sources.list.d/</code>
  
<code>sudo nano /etc/apt/sources.list.d/debian.list</code>
  
and add the following to the file:
  
<code>deb http://ftp.debian.org/debian stable main contrib non-free</code>
  
Then update the package lists from newly configured sources:
  
<code>sudo apt update</code>
  
and now install nextCloud desktop client.
  
<code>sudo apt install -y nextcloud-desktop</code>

We have provided a Python code to change the sync interval time.
  
Add this line to the crontab file to synchronize RPR’s NMEA data directory every 1 minute: 
  
<code>#to synchronize RPR’s NMEA data directory every minute</code>
  
<code>0/1 * * * * /bin/python3.7 /home/pi/RPR/pyCodes/sync_nextCloudData.py</code>
  
The streaming inveral (1 minute here) can be increased/decreased by changing <code>streaming_interval</code> variable in <code>sync_nextCloudData.py</code> and then in crontab line above. 

