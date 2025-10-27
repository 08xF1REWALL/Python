import ctypes
from ctypes import *

# --- Kernel32 DLL ---
kernel32 = windll.kernel32

# --- Basic Windows types ---
WORD = c_ushort
DWORD = c_ulong
LONG = c_long
LPBYTE = POINTER(c_ubyte)
LPTSTR = c_char_p
HANDLE = c_void_p
BYTE = c_ubyte
BOOL = c_int

# --- Constants ---
DEBUG_PROCESS = 0x00000001
CREATE_NEW_CONSOLE = 0x00000010
PROCESS_ALL_ACCESS = 0x1F0FFF
INFINITE = 0xFFFFFFFF
DBG_CONTINUE = 0x00010002

# Thread access
THREAD_ALL_ACCESS = 0x1F03FF  # common definition for THREAD_ALL_ACCESS

# Toolhelp snapshot
TH32CS_SNAPTHREAD = 0x00000004

# Context flags (x86)
CONTEXT_FULL = 0x00010007
CONTEXT_DEBUG_REGISTERS = 0x00010010

# Maximum supported extension (x86 FPU saved area)
MAXIMUM_SUPPORTED_EXTENSION = 512

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

# --- DEBUG_EVENT structure (minimal placeholder) ---
class DEBUG_EVENT(Structure):
    _fields_ = [
        ("dwDebugEventCode", DWORD),
        ("dwProcessId", DWORD),
        ("dwThreadId", DWORD),
        ("u", BYTE * 160),  # placeholder for the large union
    ]


# --- THREADENTRY32 structure for Toolhelp APIs ---
class THREADENTRY32(Structure):
    _fields_ = [
        ("dwSize", DWORD),
        ("cntUsage", DWORD),
        ("th32ThreadID", DWORD),
        ("th32OwnerProcessID", DWORD),
        ("tpBasePri", LONG),
        ("tpDeltaPri", LONG),
        ("dwFlags", DWORD),
    ]

LPTHREADENTRY32 = POINTER(THREADENTRY32)


# --- FLOATING_SAVE_AREA used inside CONTEXT (x86) ---
class FLOATING_SAVE_AREA(Structure):
    _fields_ = [
        ("ControlWord", DWORD),
        ("StatusWord", DWORD),
        ("TagWord", DWORD),
        ("ErrorOffset", DWORD),
        ("ErrorSelector", DWORD),
        ("DataOffset", DWORD),
        ("DataSelector", DWORD),
        ("RegisterArea", BYTE * 80),  # 80 bytes for floating registers
        ("Cr0NpxState", DWORD),
    ]


# --- CONTEXT structure (x86) ---
class CONTEXT(Structure):
    _fields_ = [
        ("ContextFlags", DWORD),
        ("Dr0", DWORD),
        ("Dr1", DWORD),
        ("Dr2", DWORD),
        ("Dr3", DWORD),
        ("Dr6", DWORD),
        ("Dr7", DWORD),
        ("FloatSave", FLOATING_SAVE_AREA),
        ("SegGs", DWORD),
        ("SegFs", DWORD),
        ("SegEs", DWORD),
        ("SegDs", DWORD),
        ("Edi", DWORD),
        ("Esi", DWORD),
        ("Ebx", DWORD),
        ("Edx", DWORD),
        ("Ecx", DWORD),
        ("Eax", DWORD),
        ("Ebp", DWORD),
        ("Eip", DWORD),
        ("SegCs", DWORD),
        ("EFlags", DWORD),
        ("Esp", DWORD),
        ("SegSs", DWORD),
        ("ExtendedRegisters", BYTE * MAXIMUM_SUPPORTED_EXTENSION),
    ]


# --- Function prototypes (helpful to avoid ctypes surprises) ---
kernel32.CreateProcessA.restype = BOOL
kernel32.CreateProcessA.argtypes = [LPTSTR, LPTSTR, c_void_p, c_void_p, BOOL, DWORD, c_void_p, LPTSTR, POINTER(STARTUPINFO), POINTER(PROCESS_INFORMATION)]

kernel32.OpenProcess.restype = HANDLE
kernel32.OpenProcess.argtypes = [DWORD, BOOL, DWORD]

kernel32.WaitForDebugEvent.restype = BOOL
kernel32.WaitForDebugEvent.argtypes = [POINTER(DEBUG_EVENT), DWORD]

kernel32.ContinueDebugEvent.restype = BOOL
kernel32.ContinueDebugEvent.argtypes = [DWORD, DWORD, DWORD]

kernel32.DebugActiveProcess.restype = BOOL
kernel32.DebugActiveProcess.argtypes = [DWORD]

kernel32.DebugActiveProcessStop.restype = BOOL
kernel32.DebugActiveProcessStop.argtypes = [DWORD]

# Toolhelp functions
kernel32.CreateToolhelp32Snapshot.restype = HANDLE
kernel32.CreateToolhelp32Snapshot.argtypes = [DWORD, DWORD]

kernel32.Thread32First.restype = BOOL
kernel32.Thread32First.argtypes = [HANDLE, LPTHREADENTRY32]

kernel32.Thread32Next.restype = BOOL
kernel32.Thread32Next.argtypes = [HANDLE, LPTHREADENTRY32]

kernel32.CloseHandle.restype = BOOL
kernel32.CloseHandle.argtypes = [HANDLE]

# OpenThread
kernel32.OpenThread.restype = HANDLE
kernel32.OpenThread.argtypes = [DWORD, BOOL, DWORD]

# GetThreadContext
kernel32.GetThreadContext.restype = BOOL
kernel32.GetThreadContext.argtypes = [HANDLE, POINTER(CONTEXT)]

# SetThreadContext (if you need it later)
kernel32.SetThreadContext.restype = BOOL
kernel32.SetThreadContext.argtypes = [HANDLE, POINTER(CONTEXT)]
