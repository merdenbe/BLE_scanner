import argparse
import redis

from apscheduler.schedulers.background import BlockingScheduler
from bluepy.btle import Scanner, Peripheral

from utils import ScanDelegate, updateEntry, createEntry, buildParser


SCANNING_INTERVAL= 10
OUTPUT_FILE = "default"
TARGET_ADDR = None
MIN_RSSI = None


def setGlobals(args):
  global TARGET_ADDR
  global OUTPUT_FILE
  
  if args.targetAddr is not None:
    TARGET_ADDR = args.targetAddr

  if args.outputFile is not None:
    OUTPUT_FILE = args.outputFile


def readDevice(dev):
  # Only read  devices with a specific addr 
  if TARGET_ADDR is not None and dev.getValueText(9) != TARGET_ADDR:
    return

  # Only reads devices within a range
  if MIN_RSSI is not None and dev.rssi < MIN_RSSI:
    return 

  # Either update an existing entry or create a new one  
  if r.exists(dev.addr):
    updateEntry(r, dev, SCANNING_INTERVAL, OUTPUT_FILE)
  else:
    createEntry(r, dev, OUTPUT_FILE) 


def scan(r, scanner):
  scanner.clear()
  devices = scanner.scan(1.0)
  
  for dev in devices:
    readDevice(dev)


if __name__ == "__main__":
  # Parse command line arguments 
  parser = buildParser()
  args = parser.parse_args()
  setGlobals(args)

  # Initialize database instance
  r = redis.Redis()
 
  # Initialize scanner
  scanner = Scanner().withDelegate(ScanDelegate())
  
  # Initialize scheduler 
  sched = BlockingScheduler()
  sched.add_job(lambda: scan(r, scanner), 'interval', seconds=SCANNING_INTERVAL)
  sched.start()

 
