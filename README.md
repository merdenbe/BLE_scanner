# BLE_scanner

Currently the scanner is built to run a scan every 10 seconds for all BLE
devices advertising a specific UUID. The scanner logs the appearance of 
each device in the database. If the device stays in the range of the scanner
for more than one scanning interval, then it is only logged once. 


## File Descriptions

  /requirements.txt - contains all necessary python packages 
  /scanner.py - contains the main functionality of the scanner
  /utils.py - contains utility functions used in scanner.py
  /logs - contains the log files that store scanner logs 


## Setup

These installation steps must be taken if not working on mlab_pi_0000.

1. Install Redis on pi - https://habilisbest.com/install-redis-on-your-raspberrypi

2. Install python packages
  
  $ sudo pip3 install -r requirements.txt


## Run the Scanner

$ sudo python3 scanner.py -t <UUID>


## Bugs

1. Only scan for devices based on a minimum RSSI value
2. Change the key used in the redis database to a identifier that is unchanging
   (user_id broadcasted by the advertisting app)
3. Determine protocol for when the pi's storage runs out. (Transfer to cloud
   storage)
