# printf_random.py
import pydbg
from pydbg import *
#from pydbg.defines import *
import random
import struct
import subprocess
import sys
import time
import os

# Ensure DBG_CONTINUE is available: prefer import from pydbg.defines, otherwise use fallback.
try:
    # Import dynamically to avoid static analyzers complaining about a missing pydbg.defines module
    import importlib
    _mod = importlib.import_module("pydbg.defines")
    DBG_CONTINUE = getattr(_mod, "DBG_CONTINUE", 0x00010002)
except Exception:
    # fallback value if pydbg.defines isn't available
    DBG_CONTINUE = 0x00010002


# callback for the breakpoint
def printf_randomizer(dbg):
    try:
        # Read the parameter at ESP + 0x8 (printf's first argument for cdecl)
        parameter_addr = dbg.context.Esp + 0x8
        counter_data = dbg.read_process_memory(parameter_addr, 4)
        # Unpack little-endian unsigned long
        counter = struct.unpack("<L", counter_data)[0]
        print(f"[*] Counter (original): {counter}")

        # Generate a random number 1..100 and pack
        random_counter = random.randint(1, 100)
        print(f"[*] Replacing with random value: {random_counter}")

        packed_random = struct.pack("<L", random_counter)
        dbg.write_process_memory(parameter_addr, packed_random)

    except Exception as e:
        print(f"[!] Exception in callback: {e}")

    # Continue execution
    return DBG_CONTINUE


def launch_process(path_to_exe, args=None):
    """Launch a process and return its PID.
       We use subprocess to start it without waiting.
    """
    if args:
        proc = subprocess.Popen([path_to_exe] + args)
    else:
        proc = subprocess.Popen([path_to_exe])
    # give time for process to initialize and load DLLs
    time.sleep(0.5)
    return proc.pid


def launch_python_printf_loop(python_exe=None):
    """Launch the printf_loop.py in a new Python process and return pid."""
    script_path = os.path.abspath("printf_loop.py")
    if not os.path.exists(script_path):
        print("[!] printf_loop.py not found in current directory.")
        return None
    if python_exe is None:
        python_exe = sys.executable  # same interpreter
    proc = subprocess.Popen([python_exe, script_path])
    time.sleep(0.5)
    return proc.pid


if __name__ == "__main__":
    dbg = pydbg.pydbg()
    
    print("Choose mode:")
    print("1) Attach to an existing PID (enter PID)")
    print("2) Launch Notepad and attach to it (notepad will NOT call printf)")
    print("3) Launch local printf_loop.py and attach to it (recommended)")

    choice = input("Choice (1/2/3): ").strip()

    pid = None
    if choice == "1":
        try:
            pid = int(input("Enter target PID: ").strip())
        except ValueError:
            print("[!] Invalid PID")
            sys.exit(1)

    elif choice == "2":
        notepad_path = r"C:\Windows\System32\notepad.exe"
        print(f"[*] Launching {notepad_path} ...")
        pid = launch_process(notepad_path)
        print(f"[*] Launched Notepad PID: {pid}")
        print("[!] Reminder: Notepad does not call msvcrt.printf by default.")

    elif choice == "3":
        # Launch the local printf_loop.py (recommended)
        print("[*] Launching local printf_loop.py ...")
        # Optionally override to a specific python executable (32-bit)
        pid = launch_python_printf_loop()
        if pid is None:
            sys.exit(1)
        print(f"[*] printf_loop.py launched with PID: {pid}")

    else:
        print("[!] Invalid choice")
        sys.exit(1)

    # Give the target a moment to initialize
    time.sleep(0.5)

    # Attach the debugger
    try:
        dbg.attach(pid)
    except Exception as e:
        print(f"[!] Failed to attach: {e}")
        sys.exit(1)

    print(f"[*] Attached to PID {pid}")

    # Resolve printf in msvcrt.dll
    printf_address = dbg.func_resolve("msvcrt", "printf")
    if not printf_address:
        print("[!] Could not resolve printf address in msvcrt.")
        # You may still continue but breakpoint will not be set
        sys.exit(1)

    print(f"[*] printf() address: 0x{printf_address:08X}")

    # Set breakpoint with callback
    dbg.bp_set(printf_address, description="printf_address", handler=printf_randomizer)
    print("[*] Breakpoint set on printf(). Running...")

    # Run the debugger loop
    dbg.run()
