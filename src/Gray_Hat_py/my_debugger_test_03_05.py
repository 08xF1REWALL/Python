#!/usr/bin/env python3
"""
Launch notepad (SysWOW64 32-bit), resolve printf in the remote process,
set a breakpoint at printf, and enter the debugger loop.
"""

import time
import ctypes
from ctypes import byref, c_void_p, c_char_p, c_ulong
import my_debugger_03_5 as my_debugger # your module with Debugger class

# constants for toolhelp (we redeclare here for the resolver)
TH32CS_SNAPMODULE = 0x00000008
TH32CS_SNAPMODULE32 = 0x00000010

kernel32 = ctypes.windll.kernel32

# MODULEENTRY32 structure (32-bit layout; works for 32-bit target)
class MODULEENTRY32(ctypes.Structure):
    _fields_ = [
        ("dwSize", ctypes.c_ulong),
        ("th32ModuleID", ctypes.c_ulong),
        ("th32ProcessID", ctypes.c_ulong),
        ("GlblcntUsage", ctypes.c_ulong),
        ("ProccntUsage", ctypes.c_ulong),
        ("modBaseAddr", ctypes.c_void_p),    # LPBYTE -> use void_p to hold address
        ("modBaseSize", ctypes.c_ulong),
        ("hModule", ctypes.c_void_p),
        ("szModule", ctypes.c_char * 256),
        ("szExePath", ctypes.c_char * 260),
    ]

# Helper to resolve a function address inside the remote process by:
#  1) finding the remote module base (CreateToolhelp32Snapshot + Module32First/Next)
#  2) loading the same DLL locally and using GetProcAddress to compute offset
#  3) remote_address = remote_base + (local_procaddr - local_base)
def func_resolve_remote(pid: int, dll: bytes, funcname: bytes, timeout_s: float = 5.0):
    """
    Return the address (int) of `funcname` in the remote process `pid` when the module `dll`
    is loaded there. Returns None if not found within timeout.
    """
    deadline = time.time() + timeout_s

    # Ensure prototypes exist
    kernel32.CreateToolhelp32Snapshot.restype = ctypes.c_void_p
    kernel32.Module32FirstA.restype = ctypes.c_int
    kernel32.Module32FirstA.argtypes = [ctypes.c_void_p, ctypes.POINTER(MODULEENTRY32)]
    kernel32.Module32NextA.restype = ctypes.c_int
    kernel32.Module32NextA.argtypes = [ctypes.c_void_p, ctypes.POINTER(MODULEENTRY32)]

    while time.time() < deadline:
        # Snapshot modules for the target process
        snap = kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPMODULE | TH32CS_SNAPMODULE32, pid)
        if not snap or int(snap) == -1:
            time.sleep(0.1)
            continue

        me32 = MODULEENTRY32()
        me32.dwSize = ctypes.sizeof(MODULEENTRY32)

        found = False
        if kernel32.Module32FirstA(snap, byref(me32)):
            while True:
                modname = me32.szModule.decode(errors="ignore")
                # Compare case-insensitive bytes
                if modname.lower() == dll.decode().lower():
                    remote_base = int(me32.modBaseAddr)
                    found = True
                    break
                if not kernel32.Module32NextA(snap, byref(me32)):
                    break

        kernel32.CloseHandle(snap)

        if found:
            # Load the DLL locally to compute the offset of the function
            local_handle = kernel32.LoadLibraryA(dll)
            if not local_handle:
                print(f"[*] Failed to LoadLibrary locally for {dll!r}")
                return None

            # GetProcAddress returns pointer (FARPROC)
            proc_local = kernel32.GetProcAddress(local_handle, funcname)
            if not proc_local:
                kernel32.FreeLibrary(local_handle)
                print(f"[*] GetProcAddress failed locally for {funcname!r}")
                return None

            local_base = int(local_handle)
            proc_local = int(proc_local)
            offset = proc_local - local_base
            remote_addr = remote_base + offset

            # Clean up local library handle
            kernel32.FreeLibrary(local_handle)

            return remote_addr

        # not found yet
        time.sleep(0.15)

    return None


def main():
    dbg = my_debugger.Debugger()

    # Use the requested process path (32-bit Notepad in SysWOW64)
    exe_path = b"C:\\Windows\\SysWOW64\\notepad.exe"
    print(f"[*] Launching {exe_path!r} under debugger...")
    dbg.load(exe_path)

    # After load(), the process will produce debug events; give it a short time
    # until the modules are loaded. The resolver has internal waiting, but a
    # brief pause here helps.
    time.sleep(0.5)

    pid = dbg.pid
    if not pid:
        print("[!] Debugger didn't set PID")
        return

    print(f"[*] Resolving printf in target PID {pid} ...")
    printf_addr = func_resolve_remote(pid, b"msvcrt.dll", b"printf", timeout_s=8.0)
    if not printf_addr:
        print("[!] Could not resolve printf in the target process (module not loaded or timed out).")
        return

    print(f"[*] Resolved printf at 0x{printf_addr:08X} in remote process")

    # Set breakpoint (bp_set expects an integer address)
    if dbg.bp_set(printf_addr):
        print(f"[*] Breakpoint set at 0x{printf_addr:08X}")
    else:
        print("[!] Failed to set breakpoint at printf")

    # Continue the debugger loop (this will block and handle debug events)
    print("[*] Entering debugger run loop. Interact with the target (e.g., trigger printf).")
    dbg.run()


if __name__ == "__main__":
    main()
