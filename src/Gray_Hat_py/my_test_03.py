# test.py - use 64-bit Python and run as Administrator
from my_debugger_03 import Debugger
from my_debugger_defines_03 import *

def main():
    dbg = Debugger()
    try:
        pid = int(input("Enter the PID of the process to attach to: "))
    except Exception:
        print("Invalid PID")
        return

    if not dbg.attach(pid):
        return

    printf_addr = dbg.func_resolve("msvcrt.dll", "printf")
    if not printf_addr:
        print("Could not resolve printf")
    else:
        print("[*] Address of printf: 0x%016x" % printf_addr)
        if dbg.bp_set_hw(printf_addr, 1, HW_EXECUTE):
            print("[*] Hardware breakpoint set on printf")

    try:
        dbg.run()
    except KeyboardInterrupt:
        print("[*] Debugging stopped by user")

    dbg.detach()

if __name__ == "__main__":
    main()
