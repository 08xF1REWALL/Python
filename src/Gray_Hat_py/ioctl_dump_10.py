import pickle
import driverlib
from immlib import *

def main(args):
    ioctl_list = []
    device_list = []
    imm = Debugger()
    driver = driverlib.Driver()
    
    ioctl_list = driver.getIOCTLCodes()
    if not len(ioctl_list):
        return "[*] Error! could not findIOCTL codes."
    
    device_list = driver.getDeviceNames()
    if not len(device_list):
        return "[*] Error! could not find device names."
    
    master_list = {}
    master_list['ioctl_list'] = ioctl_list
    master_list['device_list'] = device_list
    
    filename = "%s.fuzz" % imm.getDebuggedName()
    with open(filename, 'wb') as fd:
        pickle.dump(master_list, fd)
        fd.close()
        return "[*] Success! Saved IOCTL codes and device names to %s" % filename
        
    