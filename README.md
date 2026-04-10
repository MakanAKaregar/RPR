This project is licensed under the GNU General Public License v3.0 - see the LICENSE file for details.

## RPR V2.0.0
* The Raspberry Pi Reflector (RPR) is a  field-ready system for tracking water levels with cm accuracy.
* RPR V2.0.0 consists of a cost-effective **single-frequency** Global Navigation Satellite System (GNSS) module and an active patch antenna, both connected to a Raspberry/Banana Pi microcomputer.
* RPR uses GNSS Interferometric Reflectometry (GNSS-IR) technique and can be operated safely in extreme weather with lower operational costs.

## Key Advantages of the RPR System
* Cost-effective: total hardware cost is ~ 150 €, or 400–500 € with a solar power option.
* High accuracy: water level measurements with cm accuracy.
* All-weather operation: GNSS-IR has reliable performance in extreme weather conditions with minimal operational expenses.
* Real-time data: supports real-time or near real-time data transmission.
* Remote supervision: remote monitoring and control of the GNSS unit and other components.
* Simple deployment: requires only a single site visit for installation.
* No on-site calibration: operates without the need for local calibration.
* Citizen science friendly: support community involvement and citizen science initiatives and FAIR data principles.

For more information about the [RPR sensor (V1.0.0)](https://github.com/MakanAKaregar/RPR/tree/main), please check out the paper:

Karegar, M. A., Kusche, J., Geremia‐Nievinski, F., & Larson, K. M. (2022). Raspberry Pi Reflector (RPR): A low‐cost water‐level monitoring system based on GNSS interferometric reflectometry. Water Resources Research, 58(12), e2021WR031713. https://doi.org/10.1029/2021WR031713

<p align="center">
<img src="https://raw.githubusercontent.com/MakanAKaregar/RPR/v2.0.0/assets/RPRV2_components.png" width="1000"/>
</p>

The RPR V2.0.0 hardware setup consists of: (a) a Raspberry Pi (RPi) Zero/3 or 4, or Banana Pi (BPi) M5 single-board computer; (b) a u-blox Max-M10S ultra low-power GNSS receiver; (c) an external GPS antenna and (d) a 4G/LTE modem for data connectivity (if neede). This configuration is the system currently in use in several projects such as [CAMEO-WAGST](https://github.com/MakanAKaregar/CAMEO_WGAST), [DETECT B01](https://www.sfb1502.de/news-events/news/news-collector-invisible/detects-swot-team-installing-raspberry-pi-reflectors-and-micro-stations-on-rhine-bridges).

This guide includes two pre-configured images, each intended for a different hardware setup.

There are two pre-configured images available for download and use.

- **Banana Pi M5 Image:**

This image is for the Banana Pi M5 which runs a quad-core ARM Cortex-A55 CPU. It works best at sites with grid power and/or where on-site SNR data processing is needed. It runs Raspberry Pi OS Bullseye, a Debian-based Linux system (version 2022-04-09), adapted for the Banana Pi M5 and tested on it since 2022. It comes with a desktop environment and unlike RPR v1.0.0, everything is pre-configured out of the box: all libraries, code, and environment variables are ready to go.

- **Raspberry Pi Zero Image:**

This image is for the Raspberry Pi Zero, a single-core micro-computer that uses three to four times less power than the BPi M5 or RPi 4. It is a great fit for solar-powered setups where power consumption matters. Because of its limited processing power, running heavy applications like gnssrefl locally is possible but not the recommended option. Instead, NMEA data is transferred from the RPR unit to a remote server for processing. It runs Raspberry Pi OS Lite (32-bit), a Debian Bookworm-based system with no desktop environment. Like the BPi M5 image, everything comes pre-configured, all libraries, code and environment variables are ready to go.

1. Download the RPR image for either the RPi Zero or BPi M5 from the University of Bonn cloud storage:

RPR with RPi Zero: <code>https://uni-bonn.sciebo.de/s/7TZNmLZQtPXEqtN</code>

RPR with BPi M5:  <code>https://uni-bonn.sciebo.de/s/fqC4DPok9ogZtEF</code>

2. Download and install [RPi Imager](https://www.raspberrypi.com/software/) to a computer with a micro SD card reader

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
- Connect a monitor, keyboard and mouse.
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
The dongle consumes 400-500 mA (2–2.5 W). To save power, use a [USB power switch](https://thepihut.com/products/usb3-power-switch?srsltid=AfmBOoogntO6qjs-bch-UDlYGLGTQxrB2J2mGbT_Xse4x5ICotnA7HkP) to turn off the dongle when not transferring data.

6. Remote access to RRP

6.1 Via SSH
- If connected via LAN or WiFi:

Use SSH to access RPR: <code>ssh pi@<RPR_IP></code>

- If using HUAWEI USB dongle:

Use ZeroTier One for remote SSH. The image includes ZeroTier One pre-installed. On your PC, go to my.zerotier.com, sign up, create a network and obtain your Network ID.

On RPR (connected to a monitor), join your network:

<code>sudo zerotier-cli join <YOUR_NETWORK_ID></code>

If you don't see your new device in <code>my.zerotier.com</code>, the local ZeroTier identity or data may be corrupted. You can reset the identity, which will generate a new Node ID for your device.

Reset the ZeroTier identity

<code>sudo systemctl stop zerotier-one</code>

<code>sudo rm -rf /var/lib/zerotier-one</code>

<code>sudo systemctl start zerotier-one</code>

Then:

<code>sudo zerotier-cli join <YOUR_NETWORK_ID></code>

6.2 GUI remote access (only BPi M5 or RPi 4):

TeamViewer is pre-installed. To set up:

<code>sudo teamviewer passwd YOURPASSWORD</code>

<code>sudo teamviewer setup</code>

7. Connect the GNSS module

- Connect the GNSS antenna to GNSS module and then to the Pi.
- Reboot the system.

8. Data generation Details

All RPR data are stored in /home/pi/RPR/data.

- GNSS data: collected by <code>dataPicker.py</code> via serial (using <code>pyserial</code> and <code>pynmea2</code>). Data are saved as daily log files in the format <code>YYMMDD.log</code> (e.g., <code>250723.log</code> for July 23, 2025).

- CPU temperature: logged every 2 hours by <code>logCPUtemprature.py</code> for maintenance and troubleshooting. These records are saved in <code>CPUtemperature.txt</code>.

- Reboot log: reboot events and related diagnostics are logged by <code>logReboot.sh</code> and saved in <code>reboot_count.log</code>.

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



