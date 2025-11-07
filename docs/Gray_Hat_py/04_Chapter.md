# PYDBG
- content 
1. extending breakpoint handlers
2. handling application crashes and taking process snapshots. 

## Extending Breakpoint Handlers
- bp_set(address, description="",restore=True,handler=None)

## Access Violation Handlers
An access violation occurs inside a process when it attempts to access memory. it doesn’t have permission to access or in a particular way that it is not allowed. 

The faults that lead to access violations range from buffer overflows to improperly handled null pointers. From a security perspective, every access violation
should be reviewed carefully, as the violation might be exploited. 

It is crucial that the debugger trap all information that is relevant, such as the stack frame, the registers, and the instruction
that caused the violation. You can now use this information as a starting point
for writing an exploit or creating a binary patch.

## Process Snapshots
Using process snapshotting you are able to freeze a process, obtain all of its memory,
and resume the process. At any later point you can revert the process to the
point where the snapshot was taken. This can be quite handy when reverse
engineering a binary or analyzing a crash.