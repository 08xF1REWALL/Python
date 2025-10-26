from ctypes import *
from my_debugger_defines_03_2 import *

# Mapping of debug event codes to human-readable names
DEBUG_EVENT_CODES = {
    1: "CREATE_THREAD_DEBUG_EVENT",
    2: "CREATE_PROCESS_DEBUG_EVENT",
    3: "EXIT_THREAD_DEBUG_EVENT",
    4: "EXIT_PROCESS_DEBUG_EVENT",
    5: "LOAD_DLL_DEBUG_EVENT",
    6: "UNLOAD_DLL_DEBUG_EVENT",
    7: "OUTPUT_DEBUG_STRING_EVENT",
    8: "EXCEPTION_DEBUG_EVENT"
}

# Common exception codes
EXCEPTION_CODES = {
    0x80000003: "EXCEPTION_BREAKPOINT",
    0xC0000005: "EXCEPTION_ACCESS_VIOLATION",
    0xC000001D: "EXCEPTION_ILLEGAL_INSTRUCTION",
    0xC00000FD: "EXCEPTION_STACK_OVERFLOW",
}

class Debugger:
    def __init__(self):
        self.h_process = None
        self.pid = None
        self.debugger_active = False
        self.threads = {}  # track thread IDs
        self.loaded_dlls = {}  # track DLL base addresses and paths

    def load(self, path_to_exe: bytes):
        creation_flags = DEBUG_PROCESS
        startupinfo = STARTUPINFO()
        process_information = PROCESS_INFORMATION()
        startupinfo.dwFlags = 0x1
        startupinfo.wShowWindow = 0
        startupinfo.cb = sizeof(startupinfo)

        if kernel32.CreateProcessA(path_to_exe,
                                   None,
                                   None,
                                   None,
                                   False,
                                   creation_flags,
                                   None,
                                   None,
                                   byref(startupinfo),
                                   byref(process_information)):
            self.pid = process_information.dwProcessId
            self.h_process = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, self.pid)
            print(f"[*] Successfully launched process PID={self.pid}")
            self.debugger_active = True
            self.run()
        else:
            print(f"[*] Error: 0x{kernel32.GetLastError():08X}")

    def attach(self, pid):
        self.h_process = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
        if kernel32.DebugActiveProcess(pid):
            self.pid = pid
            self.debugger_active = True
            print("[*] Process attached to the debugger.")
            self.run()
            
        else:
            print("[*] Unable to attach to the process.")

    def run(self):
        print("[*] Debugger is running...")
        while self.debugger_active:
            self.get_debug_event()

    def get_debug_event(self):
        debug_event = DEBUG_EVENT()
        continue_status = DBG_CONTINUE

        if kernel32.WaitForDebugEvent(byref(debug_event), INFINITE):
            code = debug_event.dwDebugEventCode
            pid = debug_event.dwProcessId
            tid = debug_event.dwThreadId
            event_name = DEBUG_EVENT_CODES.get(code, f"UNKNOWN_EVENT({code})")

            # Handle thread creation
            if code == 1:  # CREATE_THREAD_DEBUG_EVENT
                self.threads[tid] = debug_event.u  # store placeholder
                print(f"[*] {event_name} PID={pid}, TID={tid} (thread created)")

            # Handle thread exit
            elif code == 3:  # EXIT_THREAD_DEBUG_EVENT
                self.threads.pop(tid, None)
                print(f"[*] {event_name} PID={pid}, TID={tid} (thread exited)")

            # Handle DLL load
            elif code == 5:  # LOAD_DLL_DEBUG_EVENT
                dll_base = cast(debug_event.u, POINTER(c_void_p)).contents.value
                dll_path = self.get_dll_path(dll_base)
                self.loaded_dlls[dll_base] = dll_path
                print(f"[*] {event_name} PID={pid}, TID={tid}, Base=0x{dll_base:X}, Path={dll_path}")

            # Handle DLL unload
            elif code == 6:  # UNLOAD_DLL_DEBUG_EVENT
                dll_base = cast(debug_event.u, POINTER(c_void_p)).contents.value
                path = self.loaded_dlls.pop(dll_base, "<unknown>")
                print(f"[*] {event_name} PID={pid}, TID={tid}, Base=0x{dll_base:X}, Path={path}")

            # Handle exceptions
            elif code == 8:  # EXCEPTION_DEBUG_EVENT
                exception_code = cast(debug_event.u, POINTER(DWORD)).contents.value
                exception_name = EXCEPTION_CODES.get(exception_code, f"UnknownException(0x{exception_code:X})")
                print(f"[*] {event_name} PID={pid}, TID={tid}, Exception={exception_name}")

            # Other events
            else:
                print(f"[*] {event_name} PID={pid}, TID={tid}")

            # Stop debugger on process exit
            if code == 4:  # EXIT_PROCESS_DEBUG_EVENT
                print(f"[*] Process PID={pid} exited. Stopping debugger.")
                self.debugger_active = False

            # Resume the debugged process
            kernel32.ContinueDebugEvent(pid, tid, continue_status)

    def get_dll_path(self, base_addr):
        """
        Attempt to read DLL path from memory.
        """
        buffer = create_string_buffer(260)
        read = c_size_t()
        if kernel32.ReadProcessMemory(self.h_process, base_addr, buffer, sizeof(buffer), byref(read)):
            return buffer.value.decode(errors="ignore")
        return "<unknown>"

    def detach(self):
        if kernel32.DebugActiveProcessStop(self.pid):
            print("[*] Detached from process. Exiting...")
            return True
        else:
            print("[*] Error detaching from process.")
            return False
