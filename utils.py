import json
import redis
import argparse
import os 

from bluepy.btle import DefaultDelegate
from datetime import datetime


'''
  Builds parser to intake arguments
  from the command line.
  Currently supports -t and -o
'''

def buildParser():
  parser = argparse.ArgumentParser()
  
  parser.add_argument("-t", "--targetAddr", type=str, default=None,
                      help="MAC address of target device")
  parser.add_argument("-o", "--outputFile", type=str, default="default",
                      help="file where output is logged to")

  return parser 


'''
  Logs actions performed on the database
  to a specified output file
'''

def log(time, statement, filename):
  path = "./logs/{}".format(filename)
 
  append_write = "a+" if os.path.exists(path) else "w+"
  f = open(path, append_write)

  f.write("[LOG - {}]: {}\n".format(time, statement))
  print("[LOG - {}]: {}\n".format(time, statement))

  f.close() 


'''
  Handler for newly scanned devices
'''

class ScanDelegate(DefaultDelegate):
  
  def __init__(self):
    DefaultDelegate.__init__(self)

  def handleDiscovery(self, dev, isNewDev, isNewData):
    pass  


'''
  returns the current time 
'''

def getCurrentTime():
  return datetime.timestamp(datetime.now())


'''
  Updates an existing entry for a device
  that has already been registered in
  the database
'''

def updateEntry(r, dev, scanInterval, filename):
  currentTime = getCurrentTime()
  entry = json.loads(r.get(dev.addr).decode('utf-8'))
  
  if entry["last_scanned_at"] - currentTime > 2*scanInterval:
    entry["times_scanned"] += 1

  entry["last_scanned_at"] = currentTime

  r.set(dev.addr, json.dumps(entry))
  log(currentTime, "updated {}".format(dev.addr), filename)

''' 
  Creates an entry for a newly scanned device in
  the database.
'''

def createEntry(r, dev, filename):
  currentTime = getCurrentTime()

  entry = {
    "last_scanned_at": currentTime,
    "times_scanned": 1
  }

  r.set(dev.addr, json.dumps(entry))
  log(currentTime, "created {}".format(dev.addr), filename) 
