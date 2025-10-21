# Debugging and Debugging Design
Debuggers enable you to perform runtime tracing of a process,or dynamic analysis

## General purpse CPU Registers count 8
- EAX register
1. the accumulator register, is used for performing optimized instrictions in x86 instruction are set to move data. Most operation like add, subtract, and compare. As well more specialized operations like multiplication or devision can only occur within the EAX register.
2. you can easily determine if a function call has failed or succeeded based on the value stored in the EAX register.
3. In addition we can determine what a actual value of what a function is returing.

- ECX register
1. called the count register is used for looping operations. The repeated operation could be storing a string or counting numbers. Important to understand that the ECX count downward not upward. 

```py
counter = 0
while counter < 10:
    print"loop number: %d" %counter
    counter += 1
# the code will equals 10 on the first loop and 9 on the second loop ...
```
In x86 assembly loops that process data rely on the ESI and EDI registers for efficient data manipulation. The ESI register is the source index for the data operation and holds the location of the input data stream. The EDI register points to the location where the results of data operation is stored or the destination index. ESI is used for reading and EDI is used for writing. 

- ESP and EBP are the registers stack ponter and the base pointer respectively. These registers are used for managing function calls and stack operations.
 
These registers are used for managing function calls and stack operation. When function are called the argument to the function pushed into the stack and followed by the return address. 

The ESP resigter register point to the top of the stack, and so it will point to the return address. 

The EBP register is used to point to the bottom. In some cases a compiler may user optimizations to remove the EBP register as stack frame pointer, in case of the EBP is freed up to the used like any other gerneral-purpose register.
- The EBX register is the only register is not desinged for anything specific. It can be used for extra storage.

- EIP register is the that points to the current intruction that is being executed. As the CPU moves through the binary execution code, EIP is updated to reflect the location where the execution is occurring . The Debugger must be able to easily read and modify the content of these to interact with the CPU and retriece the or modify these values.

## The Stack
Stores information about how function is called, the parameters it takes, and how it should return after it is finshed executing. The stack is a first in, last out(FILO) structure. Where aruments are pushed onto the stack for a function call and popped of the stack when function is finished. the ESP register is used to track the very top of the stack frame. and the EBP register is used to track the bottom of the stack frame. The stack grows from high memory addresses to low memory address. 

stack functions:
- push reg/imm/mem Decrements the stack pointer and stores a value on the stack
- pop reg/mem Loads a value from the stack into a register/memory and increments the stack pointer
- call label Pushes the return address (next instruction) onto the stack, then jumps to the function label
- ret Pops the return address off the stack and jumps back to it
- enter / leave
Set up / tear down stack frame (optional shorthand for push ebp + mov ebp, esp and mov esp, ebp + pop ebp)

```assembly
; Example function: add_numbers(a, b)
add_numbers:
    push ebp            ; Save old base pointer
    mov  ebp, esp       ; Create new stack frame
    mov  eax, [ebp+8]   ; Load first argument (a)
    add  eax, [ebp+12]  ; Add second argument (b)
    pop  ebp            ; Restore base pointer
    ret                 ; Return (jumps to address from stack)

; and the caller
main:
    push 5              ; Push argument b
    push 3              ; Push argument a
    call add_numbers    ; Push return address and jump
    add  esp, 8         ; Clean up arguments (2 × 4 bytes)
    ; Result is now in EAX

```

Example: 
function call in C
```c
int my_socks(colore_one, color_two, color_three);

```
```assembly
push color_three
push color_two
push color_one
call my_socks
```

## Debug Events
Debuggers run as an endless loop that waits for a debugging event to occur. When debugging event occur, the loop breaks, and a corresponding event handler is called.
When an event handler is called, the debugger halts and awaits directions on how to continue. Some of the common events that a debugger must trap are these:
1. Breakpoints
2. Memory violations
3. Exceptions gernerated by the debugged program.

## Breakpoints
The ability to halt a process that is being debugged is achived by setting breakpoints. There are three primary breakpoint types:
1. soft breakpoints
2. hardware breakpoints
3. memory breakpoints

## Soft Breakpoints
are used specifically to halt the cpu when executing instructions. A soft breakpoint us a single-byte instruction that stops executing of the debugged process and passes control to the debugger's breakpoint exception handler. to understand this. We need to know the difference between an instruction and an opcode in x86 assembly.

An assembly instruction is a high-level representation of a command for the CPU to execute. An example is 
MOV EAX, EBX this instruction tells the CPU to move the value stored in the register EBX to EXA.
opcode means operation code, is a machine language command that the CPU executes. 
0x44332211: 8BC3 MOV EAX, EBX
this shows the address, the opcodem and the high-level assemnbly instruction. In order to set a breakpoint at this address and halt the CPU, we have to swap out a single byte from the 2-bytes 8BC opcode. This single byte represents the interrupt 3(INT 3) instruction, which tells the CPU to halt. The INT 3 instruction is converted into the single-byte opcode 0xCC. Here is our previous example, before and after the breakpoint.
before:
0x44332211: 8BC3 MOV EAX, EBX
after:
0x44332211: CCC3 MOV EAX, EBX
8B swaped to CC byte
in opcode 8BC3 means  MOV EAX, EBX 

How the debugger works: When a debugger is hold to set a breakpoint at a address, it reads the first opcode byte at the requested address and stores it. Then the debugger writes the CC byte to that address. When a breakpoint, or INT3, event is triggered by the CPU interperting the CC opcode, the debugger catches it. The debugger then checks to see if the instruction pointer EIP register is pointing to an address on which it had set a breakpoint previouisly. If the address is found in the debugger's internal breakpoint list, it wirtes back the stored byte to that address so that the opcode can execute properly after the process is resumed. 

A CRC is a type of function that is used to determine
if data has been altered in any way, and it can be applied to files, memory,
text, network packets, or anything you would like to monitor for data alteration.

A CRC will take a range of values—in this case the running process’s
memory—and hash the contents.

It then compares the hashed value against a known CRC checksum to determine whether there have been changes to the data.
If the check sum is different from the checksum that is stored in fir the validation the CRC check fails. This is important to note as quite often malware will test it's running code in memory for any CRC changes and will kill itself if a failure is detected. This is a very effective technique to slow reverse engineering and prevent the use of soft breakpoints. A work around is to use hardware breakpoints.

## Hardware Breakpoints
are useful when a small number of breakpoints are desired and the debugged software itself cannot be modified. This type is set at CPU level, in special registers called debug registers. A typical register has 8 debug registers DR0-DR7. DR0-DR3 are reserved for the addresses of the break point. DR4 and DR5 are reserved and DR6 is used as the status register, which determines the type of debugging event triggered by the breakpoint once it is hit. Debug register DR7 is essentially the on/off switch for the hardware breakpoints. and also stores the different breakpoint conditions. By setting specific flags in the DR7 register, you can create breakpoint for the following conditions:

1. Break when an instruction is executed at a particular address
2. Break when data is written to an address
3. Break on reads or writes to an address but not execution
this is very useful as you have the ability to set up to four very specific conditionl breakpoints with out modifiying the running process.

Bits 0-7 are essentially the on/off switches for activating breakpoints. The L and G fields in bits 0-7 stand for local and global scope. Bits 8-15 in DR7 are not used for the normal debugging purposes that we will be exercising. Bits 16-31 determine the type and length of the breakpoint that is being set for the related debug register.

Hardware breakpoints are extremely useful, but they do come with
some limitations. Aside from the fact that you can set only four individual
breakpoints at a time, you can also only set a breakpoint on a maximum of
four bytes of data.

## Memory Breakpoints
aren't really breakpoints at all. When a debugger setting a memory breakpoint it is changing the premissions on a region, or page, of memory. A memory page is the smallest poriton of memory that an operating system handles. When a memory page is allocated, it has specific access premissions set, which dictate how the memory can be accessed.

Memory page premissions types:
    - Page excecution: this enables execution but throws an access violation if the process attempts to read or write to the page.
    - Page read: this enables the process only to read from the page; any writes or execution attempts cause an access violation
    - Page write: this allows the process to write into the page
    - Guard page: any access to a guard page results in a one time execution and then the page returns to its original status.

The page permission we are interested in is the guard page. This type
of page is quite useful for such things as separating the heap from the stack
or ensuring that a portion of memory doesn’t grow beyond an expected
boundary. It is also quite useful for halting a process when it hits a particular
section of memory.
For example, if we are reverse engineering a networked
server application, we could set a memory breakpoint on the region of
memory where the payload of a packet is stored after it’s received. This
would enable us to determine when and how the application uses received
packet contents, as any accesses to that memory page would halt the CPU,
throwing a guard page debugging exception. We could then inspect the
instruction that accessed the buffer in memory and determine what it is doing with the contents