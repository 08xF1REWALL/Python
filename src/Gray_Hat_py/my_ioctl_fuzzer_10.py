import pickle
import sys
import random
from ctypes import *

kernal32 = windll.kernel32
# Defines for Win32 API calls
GENERIC_READ  = 0x80000000
GENERIC_WRITE = 0x40000000
OPEN_EXISTING = 0x3

# open the pickle and retrive the dictionary
fd = open(sys.argv[1], 'rb')
master_list = pickle.load(fd)
ioctl_list = master_list['ioctl_list']
device_list = master_list['device_list']
fd.close()

valid_devices = []

for device_name in device_list:
    device_file = u"\\\\.\\%s" % device_name.split('\\')[::-1][0]
    print("[*] Testing device: %s" % device_file)
    device_handle = kernal32.CreateFileW(device_file,
                                          GENERIC_READ | GENERIC_WRITE,
                                          0,
                                          None,
                                          OPEN_EXISTING,
                                          0,
                                          None)
    if device_handle:
        print("[*] Success! %s opened device: %s" % (device_handle, device_file))
        if device_handle not in valid_devices:
            valid_devices.append(device_file)
        kernal32.CloseHandle(device_handle)
    else:
        print( "[*] Failed! %s NOT a valid device" % device_file)
    if not len(valid_devices):
        print("[*] No valid devices found. Exiting...")
        sys.exit(0)
    while 1:
        fd = open("my_ioctl_fuzz_output.txt", 'a')
        # Pick a random device name
        current_device = valid_devices[random.randint(0, len(valid_devices)-1)]
        fd.write("[*] Fuzzing device: %s\n" % current_device)
        # pick a random IOCTL code
        current_ioctl = ioctl_list[random.randint(0, len(ioctl_list)-1)]
        fd.write("[*] Using IOCTL code: 0x%08x\n" % current_ioctl)
        # choose a random length for the input buffer
        current_length = random.randint(1, 10000)
        fd.write("[*] Buffer length: %d\n" % current_length)
        in_buffer = "A" * current_length
        # give the IOCTL run a out buffer
        out_buffer = (c_char * current_length)()
        bytes_returned = c_ulong(current_length)
        # obtain a handle
        driver_handle = kernal32.CreateFileW(device_file
                                                , GENERIC_READ | GENERIC_WRITE
                                                , 0
                                                , None
                                                , OPEN_EXISTING
                                                , 0
                                                , None)   
        fd.write("!!FUZZ!!\n")
        # Run test cases
        result = kernal32.DeviceIoControl(driver_handle
                                            , current_ioctl
                                            , in_buffer
                                            , current_length
                                            , byref(out_buffer)
                                            , current_length
                                            , byref(bytes_returned)
                                            , None)
        fd.write("[*] Test case finished. %d bytes returned. \n\n" % bytes_returned.value)
        kernal32.CloseHandle(driver_handle)     
        