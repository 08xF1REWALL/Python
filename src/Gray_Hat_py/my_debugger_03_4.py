from ctypes import *
from my_debugger_defines_03_4 import *
import sys

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

        # CreateProcessA expects bytes (c_char_p)
        lpApplicationName = c_char_p(path_to_exe)
        if kernel32.CreateProcessA(lpApplicationName,
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
            print(f"[*] Debug event received: Code={debug_event.dwDebugEventCode}, PID={debug_event.dwProcessId}, TID={debug_event.dwThreadId}")

            # 1 = EXCEPTION_DEBUG_EVENT
            if debug_event.dwDebugEventCode == 1:
                print("[*] EXCEPTION_DEBUG_EVENT received!")
                ctx = self.get_thread_context(debug_event.dwThreadId)
                if ctx:
                    print(f"[**] EIP: 0x{ctx.Eip:08X}")

            kernel32.ContinueDebugEvent(
                debug_event.dwProcessId,
                debug_event.dwThreadId,
                continue_status
            )

    def detach(self):
        if kernel32.DebugActiveProcessStop(self.pid):
            print("[*] Finished debugging. Exiting...")
            return True
        else:
            print("[*] There was an error")
            return False

    # ------------------- Added thread helpers -------------------

    def open_thread(self, thread_id):
        """
        Open a thread handle with THREAD_ALL_ACCESS.
        Returns the thread handle (ctypes.c_void_p) or False on failure.
        """
        h_thread = kernel32.OpenThread(THREAD_ALL_ACCESS, False, thread_id)
        # On failure OpenThread returns NULL (0)
        if h_thread and int(h_thread) != 0:
            return h_thread
        else:
            print("[*] Could not obtain a valid thread handle.")
            return False

    def enumerate_threads(self):
        """
        Enumerate threads owned by the current debuggee process (self.pid).
        Returns a list of thread IDs.
        """
        if not self.pid:
            print("[*] No target process id set.")
            return []

        thread_entry = THREADENTRY32()
        thread_list = []

        snapshot = kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPTHREAD, 0)
        if snapshot and int(snapshot) != 0xFFFFFFFF and int(snapshot) != 0:
            # MUST set the size before calling Thread32First
            thread_entry.dwSize = sizeof(THREADENTRY32)
            success = kernel32.Thread32First(snapshot, byref(thread_entry))
            while success:
                if thread_entry.th32OwnerProcessID == self.pid:
                    thread_list.append(thread_entry.th32ThreadID)
                success = kernel32.Thread32Next(snapshot, byref(thread_entry))
            kernel32.CloseHandle(snapshot)
            return thread_list
        else:
            print("[*] CreateToolhelp32Snapshot failed.")
            return []

    def get_thread_context(self, thread_id):
        context = CONTEXT()
        context.ContextFlags = CONTEXT_FULL | CONTEXT_DEBUG_REGISTERS

        h_thread = self.open_thread(thread_id)
        if not h_thread:
            return False

        # 🔹 Suspendiere den Thread zuerst
        kernel32.SuspendThread(h_thread)

        res = kernel32.GetThreadContext(h_thread, byref(context))

        # 🔹 Danach wieder fortsetzen
        kernel32.ResumeThread(h_thread)
        kernel32.CloseHandle(h_thread)

        if res:
            return context
        else:
            print(f"[*] GetThreadContext failed. Error: 0x{kernel32.GetLastError():08X}")
            return False

