# IDAPYTHON SCRIPTING IDA PRO

## Functions

- Utility Functions
1. ScreenEA()
2. GetInputMD5()

- Segment Functions
1. Firstseg()
2. Nextseg()
3. SegByName()
4. SegEnd()
5. SegStart()
6. SegName()
7. Segments()

- Functions
1. Functions(long StartAddress, long EndAddress)
2. Chunks(long FunctionStartAddress)
3. LocByName(str FunctionName)
4. GetFuncOffset(long Address)
5. GetFunctionName(long Address)

- Cross References
1. CodeRefsTo(long Address, bool Flow)
2. CodeRefsFrom(long Address, bool Flow)
3. DataRefsTo(long Address)
4. DataRefsFrom(long Address)

## Debugger Hooks

```py
class DbgHook(DBG_Hooks):
    def dbg_process_start(self, pid, tid, ea, name, base, size):
        return
    def dbg_process_exit(self, pid, tid, ea, code):
        return
    
    def dbg_library_load(self, pid, tid, ea, name, base, size):
        return
    
    def dbg_bpt(self, tid, ea):
        return
# to install the hook debugger = DbgHook(); debugger.hook()    
```
- AddBpt(long Address): Adds a breakpoint at the specified address.
- GetBptQty(): Returns the number of breakpoints currently set.
- GetRegValue(string Register): Returns the value of the specified register.
- SetRegValue(string Register, long Value): Sets the specified register to the given value.

## Finding Dangerous Function Cross-References

```py
danger_funcs = ["strcpy", "sprintf", "strncpy"]
for func in danger_funcs:
    addr = LocByName(func)
    if addr != BADADDR:
        cross_refs = CodeRefsTo(addr, 0)
        print("Cross References to %s" % func)
        for ref in cross_refs:
            print("0x%08X" % ref)
            SetColor(ref, CIC_ITEM, 0x0000FF)
```

## Calculating stack Size

the stack size of particular function calls. This can tell you
whether there are just pointers being passed to a function or there are stack
allocated buffers, which can be of interest if you can control how much data
is passed into those buffers
