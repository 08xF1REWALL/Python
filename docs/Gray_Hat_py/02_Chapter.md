# Debugging and Debugging Design
General purpse CPU Registers count 8
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
