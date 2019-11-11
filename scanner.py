import redis
import json

from apscheduler.schedulers.background import BlockingScheduler
from bluepy.btle import Scanner, DefaultDelegate
from datetime import datetime


class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            pass
            # print("Discovered device".format(dev.addr))
        elif isNewData:
            pass
            # print("Received new data from".format(dev.addr))


def storeDevice(dev):
  currTime = datetime.timestamp(datetime.now()) 
  
  if r.exists(dev.addr):
    print("Editing: {}".format(dev.addr))
    entry = json.loads(r.get(dev.addr).decode('utf-8'))
    entry["last_scanned_at"] = currTime
    entry["times_scanned"] += 1
  else:
    print("Storing: {}".format(dev.addr))
    entry = {"last_scanned_at": currTime, "times_scanned": 1}
    
  r.set(dev.addr, json.dumps(entry))



def scanDevices(r, scanner):
  scanner.clear()
  devices = scanner.scan(5.0)
  
  for dev in devices:
    # print("Device {} ({}), RSSI={} dB".format(dev.addr, dev.addrType, dev.rssi))
    
    storeDevice(dev)

    '''
    for (adtype, desc, value) in dev.getScanData():
        print("  {} = {}".format(desc, value))
    '''

if __name__ == "__main__":
  # Initialize database instance
  r = redis.Redis()
 
  # Initialize scanner
  scanner = Scanner().withDelegate(ScanDelegate())
  
  # Initialize scheduler 
  sched = BlockingScheduler()
  sched.add_job(lambda: scanDevices(r, scanner), 'interval', seconds=10)
  sched.start()

 
