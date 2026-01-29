from idaapi import *

class FuncCoverage(DBG_Hooks):
    def dbg_bpt(self, tid, ea):
        print("Breakpoint hit at address: 0x{:X}".format(ea))
        return

debugger = FuncCoverage()
debugger.hook()

current_addr = ScreenEA()
for function in Functions(SegStart(current_addr), SegEnd(current_addr)):
    AddBpt(function)
    SetBptAttr(function, BPTATTR_FLAGS, 0x0)
num_breakpoints = GetBptQty()
print("Total breakpoints set: {}".format(num_breakpoints))