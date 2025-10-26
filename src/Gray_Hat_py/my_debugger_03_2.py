from ctypes import *
from my_debugger_defines_03_2 import *
# from my_debugger_defines_03_2 import kernel32, PROCESS_ALL_ACCESS, DEBUG_PROCESS, INFINITE, DBG_CONTINUE, STARTUPINFO, PROCESS_INFORMATION, DEBUG_EVENT


class Debugger:
    def __init__(self):
        self.h_process = None
        self.pid = None
        self.debugger_active = False

    def load(self, path_to_exe: bytes):
        """
        Launch a process under debugger control.
        path_to_exe must be a byte string, e.g., b"C:\\Windows\\System32\\notepad.exe"
        """
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
            print("[*] We have successfully launched the process!")
            print(f"[*] PID: {process_information.dwProcessId}")

            # Store a valid handle for future access
            self.h_process = self.open_process(process_information.dwProcessId)
            self.pid = process_information.dwProcessId
            self.debugger_active = True
            self.run()
        else:
            print(f"[*] Error: 0x{kernel32.GetLastError():08X}")

    def open_process(self, pid):
        h_process = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
        return h_process

    def attach(self, pid):
        self.h_process = self.open_process(pid)
        if kernel32.DebugActiveProcess(pid):
            self.debugger_active = True
            self.pid = int(pid)
            self.run()
        else:
            print("[*] Unable to attach to the process.")

    def run(self):
        """
        Poll the debuggee for debug events.
        """
        while self.debugger_active:
            self.get_debug_event()

    def get_debug_event(self):
        debug_event = DEBUG_EVENT()
        continue_status = DBG_CONTINUE
        if kernel32.WaitForDebugEvent(byref(debug_event), INFINITE):
            print(f"[*] Debug event received: Process ID {debug_event.dwProcessId}, Thread ID {debug_event.dwThreadId}")
            input("Press Enter to continue...")  # pause for demonstration
            kernel32.ContinueDebugEvent(
                debug_event.dwProcessId,
                debug_event.dwThreadId,
                continue_status
            )
            # For this minimal example, stop after one event
            self.debugger_active = False

    def detach(self):
        if kernel32.DebugActiveProcessStop(self.pid):
            print("[*] Finished debugging. Exiting...")
            return True
        else:
            print("[*] There was an error")
            return False
