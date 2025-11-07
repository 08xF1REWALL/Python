
"""
snapshotter.py — Python3 port of your snapshotter using pydbg.

Usage:
    python snapshotter.py "C:\\Windows\\System32\\calc.exe"

Notes:
- This script assumes you have a working pydbg installation compatible with Python3.
- Many pydbg versions differ; the script checks for methods at runtime and prints useful messages.
- Running the debugger will block in the debugger thread; interactive monitor thread accepts commands:
    snap    -> try to create a snapshot (if supported)
    restore -> try to restore snapshot (if supported)
    quit    -> terminate debugged process and exit
"""

import sys
import threading
import time

# Try to import pydbg in multiple reasonable ways so this works with
# both the "package" and the single-file versions you might have.
pydbg_class = None
DBG_CONTINUE = 0x00010002

try:
    # preferred: package style
    from pydbg import pydbg as pydbg_class
    try:
        from pydbg.defines import DBG_CONTINUE as DBG_CONTINUE
    except Exception:
        pass

except Exception:
    try:
        import pydbg as pydbg_mod
        # try to locate the class inside the single-file module
        pydbg_class = getattr(pydbg_mod, "pydbg", None)
        # try to pull defines if available
        try:
            DBG_CONTINUE = getattr(pydbg_mod, "DBG_CONTINUE", DBG_CONTINUE)
        except Exception:
            pass
        # if the earlier import succeeded, prefer that class
        if pydbg_class is None:
            # maybe the module also exported a class named "debugger" or similar
            for candidate in ("pydbg", "debugger", "PyDbg"):
                pydbg_class = getattr(pydbg_mod, candidate, pydbg_class)
    except Exception:
        pydbg_class = None

if pydbg_class is None:
    print("ERROR: Could not find a usable pydbg class in your environment.")
    print("Make sure you installed/patched the OpenRCE pydbg package for Python3.")
    sys.exit(1)


class Snapshotter:
    def __init__(self, exe_path: str):
        self.exe_path = exe_path
        self.pid = None
        self.dbg = None
        self.running = True
        self._snapshot_taken = False

        # Start the debugger thread
        pydbg_thread = threading.Thread(target=self.start_debugger, name="pydbg-thread")
        pydbg_thread.daemon = True
        pydbg_thread.start()

        # Wait until the debugger sets self.pid (or timeout)
        timeout = 10.0
        waited = 0.0
        while self.pid is None and waited < timeout:
            time.sleep(0.1)
            waited += 0.1

        if self.pid is None:
            print("[!] Timeout waiting for debugged process to start/attach.")
            # If the debugger thread failed to start the process, stop here.
            self.running = False
            return

        # Start monitor thread
        monitor_thread = threading.Thread(target=self.monitor_debugger, name="monitor-thread")
        monitor_thread.daemon = True
        monitor_thread.start()

        # Keep the main thread alive while monitor runs
        try:
            while self.running:
                time.sleep(0.2)
        except KeyboardInterrupt:
            print("\n[!] KeyboardInterrupt received. Exiting.")
            self.running = False
            try:
                if self.dbg and hasattr(self.dbg, "terminate_process"):
                    self.dbg.terminate_process()
            except Exception:
                pass

    def monitor_debugger(self):
        """
        Interactive monitor loop — accepts commands from stdin:
         - snap
         - restore
         - quit
        """
        print("[*] Monitor started. Commands: 'snap', 'restore', 'quit'")
        while self.running:
            try:
                cmd = input("Enter: 'snap','restore' or 'quit' > ").strip().lower()
            except EOFError:
                # stdin closed
                break

            if cmd == "quit":
                print("[*] Exiting the snapshotter.")
                self.running = False
                if self.dbg is not None and hasattr(self.dbg, "terminate_process"):
                    try:
                        self.dbg.terminate_process()
                    except Exception as e:
                        print(f"[!] terminate_process() raised: {e}")
                break

            elif cmd == "snap":
                if self.dbg is None:
                    print("[!] Debugger not initialized.")
                    continue
                # suspend threads
                if hasattr(self.dbg, "suspend_all_threads"):
                    print("[*] Suspending all threads.")
                    try:
                        self.dbg.suspend_all_threads()
                    except Exception as e:
                        print(f"[!] suspend_all_threads() failed: {e}")
                else:
                    print("[!] suspend_all_threads() not available in this pydbg build.")

                # take snapshot if supported
                if hasattr(self.dbg, "process_snapshot"):
                    print("[*] Obtaining snapshot.")
                    try:
                        self.dbg.process_snapshot()
                        self._snapshot_taken = True
                        print("[*] Snapshot taken successfully.")
                    except Exception as e:
                        print(f"[!] process_snapshot() failed: {e}")
                else:
                    print("[!] process_snapshot() not available in this pydbg build.")

                # resume threads
                if hasattr(self.dbg, "resume_all_threads"):
                    print("[*] Resuming operation.")
                    try:
                        self.dbg.resume_all_threads()
                    except Exception as e:
                        print(f"[!] resume_all_threads() failed: {e}")
                else:
                    print("[!] resume_all_threads() not available in this pydbg build.")

            elif cmd == "restore":
                if self.dbg is None:
                    print("[!] Debugger not initialized.")
                    continue
                if not self._snapshot_taken:
                    print("[!] No snapshot has been taken yet.")
                    continue

                # suspend threads
                if hasattr(self.dbg, "suspend_all_threads"):
                    print("[*] Suspending all threads.")
                    try:
                        self.dbg.suspend_all_threads()
                    except Exception as e:
                        print(f"[!] suspend_all_threads() failed: {e}")
                else:
                    print("[!] suspend_all_threads() not available in this pydbg build.")

                # restore snapshot
                if hasattr(self.dbg, "process_restore"):
                    print("[*] Restoring snapshot.")
                    try:
                        self.dbg.process_restore()
                        print("[*] Restore completed.")
                    except Exception as e:
                        print(f"[!] process_restore() failed: {e}")
                else:
                    print("[!] process_restore() not available in this pydbg build.")

                # resume threads
                if hasattr(self.dbg, "resume_all_threads"):
                    print("[*] Resuming operation.")
                    try:
                        self.dbg.resume_all_threads()
                    except Exception as e:
                        print(f"[!] resume_all_threads() failed: {e}")
                else:
                    print("[!] resume_all_threads() not available in this pydbg build.")

            else:
                print("[!] Unknown command:", cmd)

    def start_debugger(self):
        """
        Start the debugger and launch the target process.
        This method runs in its own thread and should not block the main thread.
        """
        try:
            print(f"[*] Starting pydbg and loading: {self.exe_path}")
            # instantiate the pydbg class
            self.dbg = pydbg_class()

            # Prefer load() if available (starts a new process under debugger)
            if hasattr(self.dbg, "load"):
                try:
                    pid = self.dbg.load(self.exe_path)
                    # some pydbg implementations return pid, some not; try to normalize
                    if pid is None:
                        # try reading from attribute
                        self.pid = getattr(self.dbg, "pid", None)
                    else:
                        self.pid = int(pid)
                except Exception as e:
                    print(f"[!] self.dbg.load() raised: {e}")
                    # try createprocess style: maybe the pydbg class exposes create_process
                    self.pid = getattr(self.dbg, "pid", None)
            else:
                # if no load(), try to spawn externally and attach
                import subprocess, os
                print("[*] pydbg.load() not found. Spawning process and attaching.")
                proc = subprocess.Popen([self.exe_path])
                time.sleep(0.2)
                self.pid = proc.pid
                try:
                    if hasattr(self.dbg, "attach"):
                        self.dbg.attach(self.pid)
                except Exception as e:
                    print(f"[!] attach() failed: {e}")

            print(f"[*] Debugging PID: {self.pid}")

            # enter debugger run loop (this may block until process exits or debugger stops)
            if hasattr(self.dbg, "run"):
                try:
                    self.dbg.run()
                except Exception as e:
                    print(f"[!] dbg.run() exited with exception: {e}")
            else:
                print("[!] dbg.run() not available in this pydbg build.")

        except Exception as e:
            print(f"[!] Exception in start_debugger(): {e}")
            self.running = False


def main(argv):
    if len(argv) < 2:
        print("Usage: python snapshotter.py \"C:\\path\\to\\exe.exe\"")
        sys.exit(1)

    exe_path = argv[1]
    Snapshotter(exe_path)


if __name__ == "__main__":
    main(sys.argv)
