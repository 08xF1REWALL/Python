from my_debugger_03_4 import Debugger
from my_debugger_defines_03_4 import kernel32, THREAD_ALL_ACCESS, CONTEXT, CONTEXT_FULL, CONTEXT_DEBUG_REGISTERS

dbg = Debugger()
dbg.load(b"C:\\Windows\\SysWOW64\\notepad.exe")
threads = dbg.enumerate_threads()
for t in threads:
    ctx = dbg.get_thread_context(t)
    if ctx:
        print(f"[**] Thread {t} EIP=0x{ctx.Eip:08X}")
