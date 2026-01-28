# Fuzzing Windows Drivers

## IOCTL 
which are special gateways that allow usermode
services or applications to access kernel devices or components. As
with any means of passing information from one application to another, we
can exploit insecure implementations of IOCTL handlers to gain escalated
privileges or completely crash a target system.

on OPENBSD is used by the bio pseudo-device driver and the bioctl utility to implement RAID management in a undefined vendor-agentic interface similar to ifconfig.

- ioctl_fuzzer.py

```py
import struct
import random 
from immlib import *

class ioclt_hook(LogBpHook):
    def __init:_(self):
        self.imm = Debugger()
        self.logfile = "C:\\ioctl_log.txt"
        LogBpHook.__init__(self)

    def run(self, regs):
         """
            We use the following offsets from the ESP register
            to trap the arguments to DeviceIoControl:
            ESP+4 -> hDevice
            ESP+8 -> IoControlCode
            ESP+C -> InBuffer
            ESP+10 -> InBufferSize
            ESP+14 -> OutBuffer
            ESP+18 -> OutBufferSize
            ESP+1C -> pBytesReturned
            ESP+20 -> Overlapped
         """
         in_buf = ""
         # read the IOCTL code
         ioctl_code = self.imm.readLong(regs['ESP'] + 8)
         # read the input buffer size
         inbuffer_size = self.imm.readLong(regs['ESP'] + 0x10)
         # find the buffer in memory to mutate 
         in_buffer_ptr = self.imm.readLong(regs['ESP'] + 0xC)
         # grap the original buffer 
         in_buffer = self.imm.readMemory(in_buffer_ptr, inbuffer_size)
         mutated_buffer = self.mutate_buffer(in_buffer)
         # write the mutated buffer back to memory
         self.imm.writeMemory(in_buffer_ptr, mutated_buffer)
         # save the teat case to the file
         self.save_test_case(ioctl_code, inbuffer_size, in_buffer, mutated_buffer)
    
    def mutate_buffer(self, buffer):
        counter = 0
        mutated_buffer = ""
        while counter < inbuffer_size:
            mutated_buffer += struct.pack("H", random.randint(0,255))[0]
            counter += 1
        return mutated_buffer

        def save_test_case(self, ioctl_code, inbuffer_size, in_buffer, mutated_buffer):
            message = "*****\n"
            message += "IOCTL Code: 0x%08X\n" % ioctl_code
            message += "Input Buffer Size: %d\n" % inbuffer_size
            message += "Original Buffer: %s\n" % repr(in_buffer)
            message += "Mutated Buffer: %s\n" % repr(mutated_buffer)
            message += "*****\n\n"
            f = open(self.logfile, "a")
            f.write(message)
            f.close()
        
        def main(args):
            imm = Debugger()
            deviceiocontrol = imm.getAddress("kernel32!DeviceIoControl")
            ioctl_hooker = ioclt_hook()
            ioctl_hooker.add("%08X" % deviceiocontrol, deviceiocontrol)
            return "[*] IOCTL Fuzzer Ready for Action!"

```

- Driverlib—The Static Analysis Tool for Drivers
is a python library designed to automate some of the tedious reverse engineering tasks required to discover key pieces of information from a driver. 

```py
import driverlib

def getDeviceName(self):
    string_list = self.imm.getReferencedStrings(self.module.getCodebase())
    for s in string_list:
        if "\\Device\\" in entry[2]:
            self.imm.log("Possiable match at address: 0x%08x" % entry[0])
            self.deviceNames.append(entry[2].split("\"")[1])
            self.imm.log("Found Device Name: %s" % self.deviceNames)
            return self.deviceNames

driver = driverlib.Driver()
driver.getDeviceName()

```

## Finding the IOCTL Dispatch Routine
Any driver that implements IOCTL interface must have an IOCTL dispatch routine that handels the processing of the various IOCTL requests. When a driver loads the first function that gets called is the DriverEntry routine. 

```c
NTSTATUS DriverEntry(IN PDRIVER_OBJECT DriverObject,
                     IN PUNICODE_STRING RegistryPath)
{
    UNICODE_STRING uDeviceName;
    UNICODE_STRING uDeviceSymlink;
    PDEVICE_OBJECT gDeviceObject;
    
    RtlInitUnicodeString(&uDeviceName, L"\\Device\\GrayHat");
    RtlInitUnicodeString(&uDeviceSymlink, L"\\DosDevices\\GrayHat");
    
    // Register the device
    IoCreateDevice(DriverObject, 0, &uDeviceName,
                   FILE_DEVICE_NETWORK, 0, FALSE,
                   &gDeviceObject);
    
    // We access the driver through its symlink
    IoCreateSymbolicLink(&uDeviceSymlink, &uDeviceName);
    
    // Setup function pointers
    DriverObject->MajorFunction[IRP_MJ_DEVICE_CONTROL] = IOCTLDispatch;
    DriverObject->DriverUnload = DriverUnloadCallback;
    DriverObject->MajorFunction[IRP_MJ_CREATE] = DriverCreateCloseCallback;
    DriverObject->MajorFunction[IRP_MJ_CLOSE] = DriverCreateCloseCallback;
    
    return STATUS_SUCCESS;
}
```
This is a very basic DriverEntry routine, but it gives you a sense of how
most devices initialize themselves. 

```assembly
mov dword ptr [REG+70h], CONSTANT
```

we will be referenced at offset 0x70 and the function pointer for the IOCTL dispatch routine will be set to CONSTANT. 
Using this instruction we can then deduce where the IOCTL-handling routine is located, and that is where we can begin searching for the various IOCTL codes. This dispatch function search is preformed by driverlib using this code:

```py
def getIOCTLDispatch(self):
    search_pattern = "mov dword ptr [REG+70h], CONST" 
    dispatch_address = self.imm.searchCommandsOnModule(self.gerCodebase(), search_pattern)

    for address in dispatch_address:
        instruction = self.imm.disasm(address[0])
        if "MOV DWORD PTR" in instruction.getResult():
            if "+70" in instruction.getResult():
                self.IOCTLDispatchFunctionAddress = instruction.getImmConst()
                self.IOCTLDispatchFunction = self.imm.getFunction(self.IOCTLDispatchFunctionAddress)
                break
    return self.IOCTLDispatchFunction
```
 This code utilizes Immunity Debugger’s powerful search API to find all
possible matches against our search criteria. Once we have found a match,
we send a Function object back that represents the IOCTL dispatch function
where our hunt for valid IOCTL codes will begin. 

## Determining Supported IOCTL Codes

The IOCTL dispatch routine commonly will perform various actions based
on the value of the code being passed in to the routine. We want to be able to
exercise each of the possible paths that are determined by the IOCTL code,
which is why we go to all the trouble of finding these values. Let’s first examine
what the C source code for a skeleton IOCTL dispatch function would look
like, and then we’ll see how to decode the assembly to retrieve the IOCTL
code values. 

```c
NTSTATUS IOCTLDispatch(IN PDEVICE_OBJECT DeviceObject, IN P)