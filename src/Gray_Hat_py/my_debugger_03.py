# my_debugger.py (x64) - Python 3
import sys
from ctypes import *
from my_debugger_defines_03 import *

kernel32 = windll.kernel32

class Debugger:
    def __init__(self):
        self.h_process = None
        self.pid = None
        self.debugger_active = False
        self.h_thread = None
        self.context = None
        self.breakpoints = {}          # address (int) -> original byte (bytes)
        self.exception = None
        self.exception_address = None
        self.first_breakpoint = True
        self.hardware_breakpoints = {} # slot -> (addr, length, condition)
        self.guarded_pages = []
        self.memory_breakpoints = {}

        system_info = SYSTEM_INFO()
        kernel32.GetSystemInfo(byref(system_info))
        self.page_size = system_info.dwPageSize

    def open_process(self, pid):
        return kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)

    def attach(self, pid):
        self.h_process = self.open_process(pid)
        if not self.h_process:
            print("[*] Could not open process. Are you running as Administrator and using matching architecture?")
            return False

        if kernel32.DebugActiveProcess(pid):
            self.debugger_active = True
            self.pid = int(pid)
            print(f"[*] Attached to process {pid}")
            return True
        else:
            print("[*] Unable to attach to the process. Error: 0x%08x" % kernel32.GetLastError())
            return False

    def run(self):
        while self.debugger_active:
            self.get_debug_event()

    def get_debug_event(self):
        debug_event = DEBUG_EVENT()
        continue_status = DBG_CONTINUE

        if kernel32.WaitForDebugEvent(byref(debug_event), INFINITE):
            self.h_thread = self.open_thread(debug_event.dwThreadId)
            self.context = self.get_thread_context(self.h_thread)

            print("Event code : %d Thread ID: %d" % (debug_event.dwDebugEventCode, debug_event.dwThreadId))

            if debug_event.dwDebugEventCode == EXCEPTION_DEBUG_EVENT:
                self.exception = debug_event.u.Exception.ExceptionRecord.ExceptionCode
                self.exception_address = cast(debug_event.u.Exception.ExceptionRecord.ExceptionAddress, c_void_p).value

                if self.exception == EXCEPTION_ACCESS_VIOLATION:
                    print("Access Violation Detected.")
                elif self.exception == EXCEPTION_BREAKPOINT:
                    continue_status = self.exception_handler_breakpoint()
                elif self.exception == EXCEPTION_GUARD_PAGE:
                    print("Guard Page access detected.")
                elif self.exception == EXCEPTION_SINGLE_STEP:
                    continue_status = self.exception_handler_single_step()

            kernel32.ContinueDebugEvent(debug_event.dwProcessId, debug_event.dwThreadId, continue_status)

    def detach(self):
        if kernel32.DebugActiveProcessStop(self.pid):
            print("[*] Finished debugging. Exiting...")
            return True
        else:
            print("There was an error stopping debugging. Error: 0x%08x" % kernel32.GetLastError())
            return False

    def open_thread(self, thread_id):
        h_thread = kernel32.OpenThread(THREAD_ALL_ACCESS, False, thread_id)
        if h_thread:
            return h_thread
        else:
            print("[*] Could not obtain a valid thread handle.")
            return None

    def enumerate_threads(self):
        thread_entry = THREADENTRY32()
        thread_list = []
        snapshot = kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPTHREAD, self.pid)

        if not snapshot or snapshot == -1:
            return thread_list

        thread_entry.dwSize = sizeof(thread_entry)
        success = kernel32.Thread32First(snapshot, byref(thread_entry))
        while success:
            if thread_entry.th32OwnerProcessID == self.pid:
                thread_list.append(thread_entry.th32ThreadID)
            success = kernel32.Thread32Next(snapshot, byref(thread_entry))
        kernel32.CloseHandle(snapshot)
        return thread_list

    def get_thread_context(self, thread_handle_or_id):
        ctx = CONTEXT()
        ctx.ContextFlags = CONTEXT_FULL | CONTEXT_DEBUG_REGISTERS

        close_after = False
        if isinstance(thread_handle_or_id, int):
            h_thread = self.open_thread(thread_handle_or_id)
            close_after = True
        else:
            h_thread = thread_handle_or_id

        if not h_thread:
            return None

        if kernel32.GetThreadContext(h_thread, byref(ctx)):
            if close_after:
                kernel32.CloseHandle(h_thread)
            return ctx
        else:
            if close_after:
                kernel32.CloseHandle(h_thread)
            return None

    def exception_handler_breakpoint(self):
        print("[*] Exception address: 0x%016x" % (self.exception_address or 0))

        if self.exception_address in self.breakpoints:
            print("[*] Hit user defined breakpoint.")
            original_byte = self.breakpoints[self.exception_address]
            # restore original byte
            self.write_process_memory(self.exception_address, original_byte)

            # adjust RIP back by 1
            self.context = self.get_thread_context(self.h_thread)
            if not self.context:
                return DBG_EXCEPTION_NOT_HANDLED

            try:
                self.context.Rip = self.context.Rip - 1
            except Exception:
                pass

            kernel32.SetThreadContext(self.h_thread, byref(self.context))
        else:
            if self.first_breakpoint:
                self.first_breakpoint = False
                print("[*] Hit the first breakpoint (process entry).")

        return DBG_CONTINUE

    def read_process_memory(self, address, length):
        buf = create_string_buffer(length)
        count = SIZE_T(0)
        if not kernel32.ReadProcessMemory(self.h_process, c_void_p(address), buf, length, byref(count)):
            return None
        return buf.raw[:count.value]

    def write_process_memory(self, address, data):
        if data is None:
            return False
        b = data if isinstance(data, (bytes, bytearray)) else data.encode('latin-1')
        length = len(b)
        count = SIZE_T(0)
        c_buf = create_string_buffer(b, length)
        if not kernel32.WriteProcessMemory(self.h_process, c_void_p(address), c_buf, length, byref(count)):
            return False
        return True

    def bp_set(self, address):
        print("[*] Setting software breakpoint at: 0x%016x" % address)
        if address in self.breakpoints:
            return True
        orig = self.read_process_memory(address, 1)
        if orig is None:
            return False
        if self.write_process_memory(address, b"\xCC"):
            self.breakpoints[address] = orig
            return True
        return False

    def func_resolve(self, dll, function):
        dllb = dll if isinstance(dll, bytes) else dll.encode('utf-8')
        funcb = function if isinstance(function, bytes) else function.encode('utf-8')
        handle = kernel32.GetModuleHandleA(dllb)
        if not handle:
            handle = kernel32.LoadLibraryA(dllb)
            if not handle:
                return None
        address = kernel32.GetProcAddress(handle, funcb)
        return address

    def bp_set_hw(self, address, length, condition):
        if length not in (1,2,4):
            return False
        length_encoding = {1:0, 2:1, 4:3}[length]
        if condition not in (HW_ACCESS, HW_EXECUTE, HW_WRITE):
            return False

        available = None
        for slot in range(4):
            if slot not in self.hardware_breakpoints:
                available = slot
                break
        if available is None:
            return False

        for thread_id in self.enumerate_threads():
            ctx = self.get_thread_context(thread_id)
            if not ctx:
                continue
            ctx.Dr7 |= (1 << (available * 2))
            if available == 0:
                ctx.Dr0 = address
            elif available == 1:
                ctx.Dr1 = address
            elif available == 2:
                ctx.Dr2 = address
            elif available == 3:
                ctx.Dr3 = address

            ctx.Dr7 |= (condition << ((available * 4) + 16))
            ctx.Dr7 |= (length_encoding << ((available * 4) + 18))

            h_thread = self.open_thread(thread_id)
            if h_thread:
                kernel32.SetThreadContext(h_thread, byref(ctx))
                kernel32.CloseHandle(h_thread)

        self.hardware_breakpoints[available] = (address, length, condition)
        return True

    def exception_handler_single_step(self):
        continue_status = DBG_EXCEPTION_NOT_HANDLED
        slot = None
        if (self.context.Dr6 & 0x1) and (0 in self.hardware_breakpoints):
            slot = 0
        elif (self.context.Dr6 & 0x2) and (1 in self.hardware_breakpoints):
            slot = 1
        elif (self.context.Dr6 & 0x4) and (2 in self.hardware_breakpoints):
            slot = 2
        elif (self.context.Dr6 & 0x8) and (3 in self.hardware_breakpoints):
            slot = 3

        if slot is None:
            return continue_status

        print("[*] Hardware breakpoint hit in slot %d" % slot)

        if self.bp_del_hw(slot):
            continue_status = DBG_CONTINUE
            print("[*] Hardware breakpoint removed from list.")

        return continue_status

    def bp_del_hw(self, slot):
        if slot not in self.hardware_breakpoints:
            return False

        for thread_id in self.enumerate_threads():
            ctx = self.get_thread_context(thread_id)
            if not ctx:
                continue
            ctx.Dr7 &= ~(1 << (slot * 2))
            if slot == 0:
                ctx.Dr0 = 0
            elif slot == 1:
                ctx.Dr1 = 0
            elif slot == 2:
                ctx.Dr2 = 0
            elif slot == 3:
                ctx.Dr3 = 0

            ctx.Dr7 &= ~(3 << ((slot * 4) + 16))
            ctx.Dr7 &= ~(3 << ((slot * 4) + 18))

            h_thread = self.open_thread(thread_id)
            if h_thread:
                kernel32.SetThreadContext(h_thread, byref(ctx))
                kernel32.CloseHandle(h_thread)

        del self.hardware_breakpoints[slot]
        return True

    def bp_set_mem(self, address, size):
        mbi = MEMORY_BASIC_INFORMATION()
        if kernel32.VirtualQueryEx(self.h_process, c_void_p(address), byref(mbi), sizeof(mbi)) < sizeof(mbi):
            return False

        # align to pages and apply PAGE_GUARD
        base = cast(mbi.BaseAddress, c_void_p).value
        end = address + size
        current = base
        while current <= end:
            self.guarded_pages.append(c_void_p(current))
            old_prot = DWORD(0)
            if not kernel32.VirtualProtectEx(self.h_process, c_void_p(current), SIZE_T(self.page_size), mbi.Protect | PAGE_GUARD, byref(old_prot)):
                return False
            current += self.page_size

        self.memory_breakpoints[address] = (address, size, mbi)
        return True
