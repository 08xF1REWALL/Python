#!/usr/bin/env python3
"""
danger_monitor.py

Python3 port / fixed version of the original PyDbg script that:
 - sets breakpoints on a set of "dangerous" functions (e.g. strcpy)
 - when such a function is hit, prints a small stack window and optionally snapshots
 - on access violation, bins the crash and single-steps a few instructions for inspection

Note: This depends on a working pydbg package compatible with Python3.
"""

import sys
import traceback

# --- robust pydbg import (works with package or single-file pydbg.py) ---
pydbg_class = None
try:
    # try package style
    from pydbg import pydbg as pydbg_class
    from pydbg.defines import *
except Exception:
    try:
        import pydbg as pydbg_mod  # single-file install
        # find a plausible class inside the module
        for cand in ("pydbg", "debugger", "PyDbg"):
            if hasattr(pydbg_mod, cand):
                pydbg_class = getattr(pydbg_mod, cand)
                break
        # import defines constants if present
        try:
            # try module-level constants
            EXCEPTION_ACCESS_VIOLATION = getattr(pydbg_mod, "EXCEPTION_ACCESS_VIOLATION", 0xC0000005)
            EXCEPTION_SINGLE_STEP = getattr(pydbg_mod, "EXCEPTION_SINGLE_STEP", 0x80000004)
            DBG_CONTINUE = getattr(pydbg_mod, "DBG_CONTINUE", 0x00010002)
            DBG_EXCEPTION_NOT_HANDLED = getattr(pydbg_mod, "DBG_EXCEPTION_NOT_HANDLED", 0x80010001)
        except Exception:
            EXCEPTION_ACCESS_VIOLATION = 0xC0000005
            EXCEPTION_SINGLE_STEP = 0x80000004
            DBG_CONTINUE = 0x00010002
            DBG_EXCEPTION_NOT_HANDLED = 0x80010001
    except Exception:
        pydbg_class = None
        EXCEPTION_ACCESS_VIOLATION = 0xC0000005
        EXCEPTION_SINGLE_STEP = 0x80000004
        DBG_CONTINUE = 0x00010002
        DBG_EXCEPTION_NOT_HANDLED = 0x80010001

if pydbg_class is None:
    print("ERROR: Could not locate a usable pydbg class. Make sure pydbg is installed/patched for Python3.")
    sys.exit(1)


# Try to import utils.crash_binning if available (not mandatory)
crash_binning = None
try:
    import utils
    if hasattr(utils, "crash_binning"):
        crash_binning = utils.crash_binning
except Exception:
    # it's optional — warn but continue
    print("[!] utils.crash_binning not available. Crash binning will be skipped.")


# Configuration
MAX_INSTRUCTIONS = 10

dangerous_functions = {
    "strcpy": "msvcrt.dll",
    "strncpy": "msvcrt.dll",
    "sprintf": "msvcrt.dll",
    "vsprintf": "msvcrt.dll",
}

# resolved mapping: address (int) -> function_name (str)
dangerous_functions_resolved = {}

# runtime state
crash_encountered = False
instruction_count = 0


def safe_smart_deref(dbg, addr):
    """Wrapper for dbg.smart_dereference with safe error handling."""
    try:
        val = dbg.smart_dereference(addr)
        return val
    except Exception:
        try:
            # fallback: read_process_memory a DWORD
            data = dbg.read_process_memory(addr, 4)
            return data
        except Exception:
            return None


def danger_handler(dbg):
    """
    Called when one of the dangerous function breakpoints is hit.
    We print a small window of the stack and optionally take a snapshot.
    """
    try:
        eip = int(dbg.context.Eip)
        func_name = dangerous_functions_resolved.get(eip, "<unknown>")
        print(f"[*] Hit dangerous function: {func_name} @ 0x{eip:08X}")
        print("=" * 60)

        # print a small stack window: from ESP to ESP + 20 (bytes)
        esp = int(dbg.context.Esp)
        esp_offset = 0
        while esp_offset <= 20:
            addr = esp + esp_offset
            param = safe_smart_deref(dbg, addr)
            print(f"[ESP + {esp_offset:>2}] (0x{addr:08X}) => {repr(param)}")
            esp_offset += 4

        print("=" * 60)
        # Attempt to snapshot (if supported)
        if hasattr(dbg, "suspend_all_threads") and hasattr(dbg, "process_snapshot") and hasattr(dbg, "resume_all_threads"):
            try:
                print("[*] Suspending all threads...")
                dbg.suspend_all_threads()
            except Exception as e:
                print(f"[!] suspend_all_threads() failed: {e}")

            try:
                print("[*] Taking process snapshot...")
                dbg.process_snapshot()
            except Exception as e:
                print(f"[!] process_snapshot() failed: {e}")

            try:
                print("[*] Resuming all threads...")
                dbg.resume_all_threads()
            except Exception as e:
                print(f"[!] resume_all_threads() failed: {e}")
        else:
            print("[!] Snapshot API not available in this pydbg build.")

    except Exception as ex:
        print(f"[!] Exception in danger_handler: {ex}")
        traceback.print_exc()

    return DBG_CONTINUE


def access_violation_handler(dbg):
    """
    Handle access violation exceptions.
    We attempt to bin the crash and, for second-chance exceptions,
    restore the process to the previously taken snapshot and single-step a few instructions.
    """
    global crash_encountered, instruction_count

    # Determine if this is a first-chance exception (let other handlers see it)
    first_chance = True
    try:
        # many pydbg wrappers provide a nested structure; try a few ways
        first_chance = bool(dbg.dbg.u.Exception.dwFirstChance)
    except Exception:
        try:
            first_chance = bool(dbg.dbg.u.Exception.dwFirstCha)
        except Exception:
            # fallback: if cannot determine, treat as second-chance to proceed
            first_chance = False

    if first_chance:
        # Let it pass to the program/other handlers first
        print("[*] Access violation (first-chance) at EIP 0x%08x" % int(dbg.context.Eip))
        return DBG_EXCEPTION_NOT_HANDLED

    # second-chance: collect crash info
    try:
        print("[*] Access violation (second-chance) at EIP 0x%08x" % int(dbg.context.Eip))
        if crash_binning is not None:
            try:
                crash_bin = crash_binning.crash_binning()
                crash_bin.record_crash(dbg)
                try:
                    print(crash_bin.crash_synopsis())
                except Exception:
                    print("[*] Crash synopsis unavailable.")
            except Exception as e:
                print(f"[!] crash_binning failed: {e}")
        else:
            print("[!] No crash_binning available; skipping recording.")
    except Exception as ex:
        print(f"[!] Exception while recording crash: {ex}")
        traceback.print_exc()

    # If we haven't already restored, try to restore to the snapshot and set single-stepping
    if not crash_encountered:
        if hasattr(dbg, "suspend_all_threads"):
            try:
                print("[*] Suspending all threads.")
                dbg.suspend_all_threads()
            except Exception as e:
                print(f"[!] suspend_all_threads failed: {e}")

        if hasattr(dbg, "process_restore"):
            try:
                print("[*] Restoring process snapshot.")
                dbg.process_restore()
                crash_encountered = True
            except Exception as e:
                print(f"[!] process_restore failed: {e}")
        else:
            print("[!] process_restore() not available in this pydbg build.")

        # Set single-step on each thread so we can log a few instructions
        try:
            thread_list = dbg.enumerate_threads() if hasattr(dbg, "enumerate_threads") else []
            for thread_id in thread_list:
                try:
                    print(f"[*] Setting single step for thread: 0x{thread_id:08x}")
                    h_thread = dbg.open_thread(thread_id) if hasattr(dbg, "open_thread") else None
                    dbg.single_step(True, h_thread) if hasattr(dbg, "single_step") else None
                    if hasattr(dbg, "close_handle") and h_thread:
                        dbg.close_handle(h_thread)
                except Exception as e:
                    print(f"[!] Could not set single-step on thread {thread_id}: {e}")
        except Exception as e:
            print(f"[!] enumerate_threads() failed: {e}")

        # Resume threads (so single-step events will start firing)
        if hasattr(dbg, "resume_all_threads"):
            try:
                dbg.resume_all_threads()
            except Exception as e:
                print(f"[!] resume_all_threads failed: {e}")

        return DBG_CONTINUE

    else:
        # Already handled before; terminate to avoid loops
        print("[*] Crash was already encountered; terminating process.")
        try:
            dbg.terminate_process()
        except Exception as e:
            print(f"[!] terminate_process failed: {e}")
        return DBG_EXCEPTION_NOT_HANDLED


def single_step_handler(dbg):
    """
    Called on single-step exceptions (we enabled these after restoring).
    Disassemble and print up to MAX_INSTRUCTIONS then disable single-step.
    """
    global instruction_count

    try:
        if not crash_encountered:
            # nothing to do
            return DBG_CONTINUE

        if instruction_count >= MAX_INSTRUCTIONS:
            # disable single stepping globally if API available
            try:
                dbg.single_step(False)
            except Exception:
                pass
            return DBG_CONTINUE

        # Disassemble current instruction
        try:
            instr = dbg.disasm(dbg.context.Eip)
        except Exception:
            instr = "<disasm-unavailable>"

        print("#%d\t0x%08x : %s" % (instruction_count, int(dbg.context.Eip), instr))
        instruction_count += 1

        # keep single-stepping
        try:
            dbg.single_step(True)
        except Exception:
            pass

    except Exception as ex:
        print(f"[!] Exception in single_step_handler: {ex}")
        traceback.print_exc()

    return DBG_CONTINUE


def main():
    global dangerous_functions_resolved

    try:
        dbg = pydbg_class()
    except Exception as e:
        print(f"[!] Failed to instantiate pydbg: {e}")
        traceback.print_exc()
        return

    # Ask user for PID
    try:
        pid = int(input("Enter the PID you wish to monitor: ").strip())
    except Exception:
        print("[!] Invalid PID.")
        return

    # Attach
    try:
        dbg.attach(pid)
    except Exception as e:
        print(f"[!] Failed to attach to PID {pid}: {e}")
        traceback.print_exc()
        return

    # Resolve dangerous functions and set breakpoints
    for fname, module in dangerous_functions.items():
        try:
            func_address = dbg.func_resolve(module, fname)
            if not func_address:
                print(f"[!] Could not resolve {fname} in {module}")
                continue
            print(f"[*] Resolved breakpoint: {fname} -> 0x{func_address:08x}")
            # set the breakpoint; store mapping from address to function name
            dbg.bp_set(func_address, handler=danger_handler)
            dangerous_functions_resolved[int(func_address)] = fname
        except Exception as e:
            print(f"[!] Error resolving/setting bp for {fname}: {e}")
            traceback.print_exc()

    # Register exception callbacks
    try:
        dbg.set_callback(EXCEPTION_ACCESS_VIOLATION, access_violation_handler)
        dbg.set_callback(EXCEPTION_SINGLE_STEP, single_step_handler)
    except Exception as e:
        print(f"[!] Could not set exception callbacks: {e}")
        traceback.print_exc()
        # still attempt to run

    # Enter debugger loop
    try:
        print("[*] Entering debugger loop. Press Ctrl-C here to exit the monitor.")
        dbg.run()
    except KeyboardInterrupt:
        print("\n[!] KeyboardInterrupt received. Exiting.")
    except Exception as e:
        print(f"[!] dbg.run() exited with exception: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    main()
