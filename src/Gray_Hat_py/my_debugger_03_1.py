import ctypes
from ctypes import *

kernel32 = ctypes.windll.kernel32

# --- Define Windows types ---
WORD = c_ushort
DWORD = c_ulong
LPBYTE = POINTER(c_ubyte)
LPTSTR = POINTER(c_char)
HANDLE = c_void_p

# --- Constants ---
DEBUG_PROCESS = 0x00000001
CREATE_NEW_CONSOLE = 0x00000010

# --- STARTUPINFO structure ---
class STARTUPINFO(Structure):
    _fields_ = [
        ("cb", DWORD),
        ("lpReserved", LPTSTR),
        ("lpDesktop", LPTSTR),
        ("lpTitle", LPTSTR),
        ("dwX", DWORD),
        ("dwY", DWORD),
        ("dwXSize", DWORD),
        ("dwYSize", DWORD),
        ("dwXCountChars", DWORD),
        ("dwYCountChars", DWORD),
        ("dwFillAttribute", DWORD),
        ("dwFlags", DWORD),
        ("wShowWindow", WORD),
        ("cbReserved2", WORD),
        ("lpReserved2", LPBYTE),
        ("hStdInput", HANDLE),
        ("hStdOutput", HANDLE),
        ("hStdError", HANDLE),
    ]

# --- PROCESS_INFORMATION structure ---
class PROCESS_INFORMATION(Structure):
    _fields_ = [
        ("hProcess", HANDLE),
        ("hThread", HANDLE),
        ("dwProcessId", DWORD),
        ("dwThreadId", DWORD),
    ]

# --- Debugger class ---
kernel32 = windll.kernel32

class Debugger:
    def __init__(self):
        pass

    def load(self, path_to_exe: bytes):
        """
        Launches a process for debugging using CreateProcessA().
        path_to_exe must be a bytes string, e.g. b"calc.exe"
        """
        creation_flags = DEBUG_PROCESS

        startupinfo = STARTUPINFO()
        process_information = PROCESS_INFORMATION()

        startupinfo.dwFlags = 0x1
        startupinfo.wShowWindow = 0x0
        startupinfo.cb = sizeof(startupinfo)

        success = kernel32.CreateProcessA(
            path_to_exe,              # lpApplicationName
            None,                     # lpCommandLine
            None,                     # lpProcessAttributes
            None,                     # lpThreadAttributes
            False,                    # bInheritHandles
            creation_flags,           # dwCreationFlags
            None,                     # lpEnvironment
            None,                     # lpCurrentDirectory
            byref(startupinfo),       # lpStartupInfo
            byref(process_information) # lpProcessInformation
        )

        if success:
            print("[*] Successfully launched process!")
            print(f"[*] PID: {process_information.dwProcessId}")
        else:
            print(f"[*] Error: 0x{kernel32.GetLastError():08X}")

if __name__ == "__main__":
    dbg = Debugger()
    dbg.load(b"C:\\Windows\\System32\\notepad.exe")
