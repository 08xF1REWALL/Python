from ctypes import *
from my_debugger_defines_03_4 import *
import sys

kernel32 = windll.kernel32

class Debugger:
    def __init__(self):
        self.h_process = None
        self.pid = None
        self.debugger_active = False
        self.h_thread = None
        self.context = None
        self.breakpoints = {}

    # ---------------- Process & Thread ----------------

    def load(self, path_to_exe: bytes):
        creation_flags = DEBUG_PROCESS
        startupinfo = STARTUPINFO()
        process_information = PROCESS_INFORMATION()
        startupinfo.dwFlags = 0x1
        startupinfo.wShowWindow = 0
        startupinfo.cb = sizeof(startupinfo)
        lpApplicationName = c_char_p(path_to_exe)

        if kernel32.CreateProcessA(
            lpApplicationName, None, None, None, False,
            creation_flags, None, None,
            byref(startupinfo), byref(process_information)
        ):
            print("[*] We have successfully launched the process!")
            print(f"[*] PID: {process_information.dwProcessId}")
            self.h_process = self.open_process(process_information.dwProcessId)
            self.pid = process_information.dwProcessId
            self.debugger_active = True
            self.run()
        else:
            print(f"[*] Error: 0x{kernel32.GetLastError():08X}")

    def open_process(self, pid):
        return kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)

    def attach(self, pid):
        self.h_process = self.open_process(pid)
        if kernel32.DebugActiveProcess(pid):
            self.debugger_active = True
            self.pid = int(pid)
            self.run()
        else:
            print("[*] Unable to attach to the process.")

    def run(self):
        while self.debugger_active:
            self.get_debug_event()

    def get_debug_event(self):
        debug_event = DEBUG_EVENT()
        continue_status = DBG_CONTINUE
        if kernel32.WaitForDebugEvent(byref(debug_event), INFINITE):
            print(f"[*] Debug event received: Code={debug_event.dwDebugEventCode}, PID={debug_event.dwProcessId}, TID={debug_event.dwThreadId}")

            if debug_event.dwDebugEventCode == 1:  # EXCEPTION_DEBUG_EVENT
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

    # ---------------- Thread Helpers ----------------

    def open_thread(self, thread_id):
        h_thread = kernel32.OpenThread(THREAD_ALL_ACCESS, False, thread_id)
        if h_thread and int(h_thread) != 0:
            return h_thread
        else:
            print("[*] Could not obtain a valid thread handle.")
            return False

    def enumerate_threads(self):
        if not self.pid:
            print("[*] No target process id set.")
            return []

        thread_entry = THREADENTRY32()
        thread_list = []
        snapshot = kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPTHREAD, 0)
        if snapshot and int(snapshot) not in (0, 0xFFFFFFFF):
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

        kernel32.SuspendThread(h_thread)
        res = kernel32.GetThreadContext(h_thread, byref(context))
        kernel32.ResumeThread(h_thread)
        kernel32.CloseHandle(h_thread)

        if res:
            return context
        else:
            print(f"[*] GetThreadContext failed. Error: 0x{kernel32.GetLastError():08X}")
            return False

    # ---------------- Memory ----------------

    def read_process_memory(self, address, length):
        read_buf = create_string_buffer(length)
        bytes_read = c_ulong(0)
        if not kernel32.ReadProcessMemory(self.h_process, c_ulong(address), read_buf, length, byref(bytes_read)):
            return False
        return read_buf.raw[:bytes_read.value]

    def write_process_memory(self, address, data: bytes):
        length = len(data)
        count = c_ulong(0)
        c_data = c_char_p(data)
        if not kernel32.WriteProcessMemory(self.h_process, c_ulong(address), c_data, length, byref(count)):
            return False
        return True

    # ---------------- Breakpoints ----------------

    def bp_set(self, address):
        if address in self.breakpoints:
            return True
        try:
            original_byte = self.read_process_memory(address, 1)
            if original_byte is False:
                print(f"[*] Failed to read memory at 0x{address:X}")
                return False
            if not self.write_process_memory(address, b"\xCC"):
                print(f"[*] Failed to write INT3 at 0x{address:X}")
                return False
            self.breakpoints[address] = (address, original_byte)
            return True
        except Exception as e:
            print(f"[*] Exception in bp_set: {e}")
            return False

    # ---------------- Function Resolver ----------------

    def func_resolve(self, dll: bytes, function: bytes):
        handle = kernel32.GetModuleHandleA(dll)
        if not handle:
            print(f"[*] Could not get handle for {dll.decode()}")
            return None
        address = kernel32.GetProcAddress(handle, function)
        kernel32.CloseHandle(handle)
        return address
