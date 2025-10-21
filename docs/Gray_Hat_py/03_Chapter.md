# Building a Windows Debugger

the most important flags that are important for
creating a process under a debugger.

lpApplicationName, lpCommandLine, dwCreationFlags, lpStartupInfo, and lpProcessInformation.

all others can be set to NULL

- lpApplicationName, lpCommandLine: parameters are used for setting the path to the executable we wish to run and
any command-line arguments it accepts.
- dwCreationFlags: parameter takes a special value that indicates that the process should be started as a debugged process. 
- lpStartupInfo, and lpProcessInformation: are pointers to structs(STARTUPINFO and PROCESS_INFORMATION) that dictate how the process should be started as well as provide importent information regarding the process after it has been seccessfully started.

```C
BOOL WINAPI CreateProcessA(
 LPCSTR lpApplicationName,
 LPTSTR lpCommandLine,
 LPSECURITY_ATTRIBUTES lpProcessAttributes,
 LPSECURITY_ATTRIBUTES lpThreadAttributes,
 BOOL bInheritHandles,
 DWORD dwCreationFlags,
 LPVOID lpEnvironment,
 LPCTSTR lpCurrentDirectory,
 LPSTARTUPINFO lpStartupInfo,
 LPPROCESS_INFORMATION lpProcessInformation
);
```