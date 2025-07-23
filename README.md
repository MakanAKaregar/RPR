## RPR V2.0.0
* The Raspberry Pi Reflector (RPR) is a  field-ready system for tracking water levels with centimeter level accuracy
* RPR consists of a cost-effective single-frequency Global Navigation Satellite System (GNSS) module and a navigation antenna, both connected to a Raspberry Pi microcomputer.
* RPR uses GNSS Interferometric Reflectometry (GNSS-IR) technique and can be operated safely in extreme weather with lower operational costs.
* 
## Key Advantages of the RPR System
* Cost-effective: Total hardware cost is ~ 150 €, or 400–500 € with a solar power option.
* High accuracy: Provides water level measurements with centimeter-level precision.
* All-weather operation: Designed for reliable performance in extreme weather conditions, with minimal operational expenses.
* Real-time data: Supports real-time or near real-time data transmission.
* Remote supervision: Enables remote monitoring and control of the GNSS unit and other components.
* Simple deployment: Requires only a single site visit for installation.
* No on-site calibration: Operates without the need for local calibration.
* Citizen science friendly: Designed to support community involvement and citizen science initiatives.

For more information about the RPR sensor (V1.0.0), please check out our paper:

Karegar, M.A., Kusche, J., Nievinski, F.G., Larson, K.M. (2022). Raspberry Pi Reflector (RPR): a Low-cost Water-level Monitoring System based on GNSS Interferometric Reflectometry, Water Resources Research (in press), https://doi.org/10.1029/2021WR031713 

<p align=center>
<img src="https://github.com/MakanAKaregar/RPR/blob/main/Figure2.png" width="600"/>
</p>
The RPR hardware setup consists of: (a) a Raspberry Pi (RPi) Zero/3 or 4, or Banana Pi (BPi) M5 single-board computer; (b) a u-blox Max-M10S ultra low-power GNSS receiver; (c) an external GPS antenna; and (d) a 4G/LTE modem for data connectivity (if neede). This configuration reflects the system currently in use.

This guide includes two pre-configured images, each intended for a different hardware setup.

There are two pre-configured images available for download and use.

- **Banana Pi M5 Image:** 

This image is for the Banana Pi M5, which features a quad-core ARM Cortex-A55 CPU. This configuration is best suited for sites with access to the power grid and/or a need for on-site SNR data processing. This image contains Raspberry Pi Operating System (OS) Bullseye, a Debian-based Linux distribution (version dated 2022-04-09) compatible with the Banana Pi M5 and has been tested on this device since 2022. This image comes with a desktop environment. In contrast to RPR version 1.0.0, this image comes pre-configured with all necessary libraries, code, and environment variables required for the RPR system. 

- **Raspberry Pi Zero Image:**

This image is intended for the Raspberry Pi Zero, a single-core micro-computer that consumes three to four times less power than the BPi M5 or RPi 4. This makes it highly suitable for solar-powered applications where power management is crucial. Due to its limited processing power, the Raspberry Pi Zero cannot run computationally intensive applications like gnssrefl locally. Instead, NMEA data should be transferred from the RPR unit to a remote server for processing. This image contains Raspberry Pi OS Lite (32-bit), a Debian Bookworm-based version without a desktop environment.  This image also comes pre-configured with all necessary libraries, code, and environment variables required for the RPR system.

1. Download image from GitHub using git commad:

 <code>git clone https://github.com/MakanAKaregar/RPR.git </code>

2. Download and install RPi Imager to a computer with a micro SD card reader

Go to:  <code>https://www.raspberrypi.com/software/ </code>. Download and install the version for your operating system (Windows, macOS, Linux).

3. Flash a custom RPi/BPi image to an SD Card 

- Insert your SD card into your computer’s SD card reader.
- Open Raspberry Pi Imager.
- Click “Choose OS” > scroll down and select “Use custom”.
- Browse to your custom .img file and select it.
- Click “Choose Storage” and select your SD card.
- Click “Write” to flash the image.
  
4. Configure RPR:
- Insert the SD card into the BPi M5 or RPi.
- Connect a monitor, keyboard, and mouse.
- Use the correct HDMI cable/adapter for your device.
- Plug in the power supply
- Login using:
  - Username: <code>pi</code>
  
  - Password: <code>RPRgnssir</code>

- Run the following command to change the password:

  <code>passwd</code>

5. Network connectivity options for RPR

- BPi M5: LAN (Ethernet) socket available.
- RPi 4: LAN (Ethernet) and WiFi available.
- RPi Zero: No built-in LAN or WiFi. Use a USB dongle.

**Recommended USB Dongle:**
  
- HUAWEI E3372h-320 (4G/LTE modem, plug-and-play, compatible with Raspbian OS, supports external antenna).

### Note:
The dongle consumes 400–500 mA (2–2.5 W). To save power, use a USB switch to turn off the dongle when not transferring data.

6. Remote access to RRP
   
6.1 Via SSH
- If connected via LAN or WiFi:
  
Use SSH to access RPR: <code>ssh pi@<RPR_IP></code>

- If using HUAWEI USB dongle:
  
Use ZeroTier One for remote SSH. The image includes ZeroTier One pre-installed. On your PC, go to my.zerotier.com, sign up, create a network and obtain your Network ID.

On RPR (connected to a monitor), join your network:

<code>sudo zerotier-cli join <YOUR_NETWORK_ID></code>

6.2 GUI remote access (only BPi M5 or RPi 4):

TeamViewer is pre-installed. To set up:

<code>sudo teamviewer passwd YOURPASSWORD</code>

<code>sudo teamviewer setup</code>

7. Connect the GNSS module

- Connect the GNSS antenna to GNSS module and then to the Pi.
- Reboot the system.
- 
8. Data generation Details
  
All RPR data are stored in /home/pi/RPR/data.

- GNSS data: Collected by <code>dataPicker.py</code> via serial (using <code>pyserial</code> and <code>pynmea2</code>). Data are saved as daily log files in the format <code>YYMMDD.log</code> (e.g., <code>250723.log</code> for July 23, 2025).

- CPU temperature: Logged every 2 hours by <code>logCPUtemprature.py</code> for maintenance and troubleshooting. These records are saved in <code>CPUtemperature.txt</code>.

- Reboot log: Reboot events and related diagnostics are logged by <code>logReboot.sh</code> and saved in <code>reboot_count.log</code>.

- Solar data: Logged by <code>logSolar.py</code> to monitor solar power and battery system performance every three hours (if used in RPi Zero). Data are saved in <code>solar_log.txt</code>.

 9. View/modify crontab jobs

 The cron jon include three main part:

### Power management cron job

The following cron jobs handle power management on the RPR system.  

| Schedule   | Task Command                                         | Description                                                                          |
|------------|------------------------------------------------------|--------------------------------------------------------------------------------------|
| `@reboot`  | `/home/pi/RPR/pyCodes/logReboot.sh`                  | Logs every system reboot event to `reboot_count.log` for diagnostics.                |
| `@reboot`  | `python3.11 /home/pi/RPR/pyCodes/packTransmitCron.py`| Compresses and transmits the previous day's data to a remote server after reboot.    |
| `@reboot`  | `python3.11 /home/pi/RPR/pyCodes/powerUSBdongle.py`  | Powers on the USB dongle and keeps it on for 600 seconds after every reboot.         |

### Data transmission cron job

The following cron jobs handle daily data transmission for the RPR system.

| Schedule      | Task Command                                         | Description                                                                      |
|---------------|------------------------------------------------------|----------------------------------------------------------------------------------|
| `03 02 * * *` | `python3.11 /home/pi/RPR/pyCodes/powerUSBdongle.py`  | Powers on the USB dongle daily at 02:03 AM to prepare for data transfer.         |
| `05 02 * * *` | `python3.11 /home/pi/RPR/pyCodes/packTransmitCron.py`| Compresses and transmits the daily RPR file to a remote server at 02:05 AM.      |

### Maintenance wake-up cron job

This cron job schedules a daily maintenance wake-up for the RPR system.

| Schedule      | Task Command                                         | Description                                                                                  |
|---------------|------------------------------------------------------|----------------------------------------------------------------------------------------------|
| `30 09 * * *` | `python3.11 /home/pi/RPR/pyCodes/powerUSBdongle.py`  | Powers on the USB dongle at 09:30 AM daily for routine maintenance and remote access (5 min). |



