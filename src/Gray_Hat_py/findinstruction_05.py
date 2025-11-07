# imm_search.py  -- intended to run inside Immunity Debugger environment (immlib)
from immlib import *

def main(args):
    imm = Debugger()

    # join the passed arguments into an assembly instruction string
    search_code = " ".join(args)

    # assemble into machine code bytes (Immunity provides Assemble)
    search_bytes = imm.Assemble(search_code)

    # search returns a list of addresses
    search_results = imm.Search(search_bytes)

    for hit in search_results:
        # Retrieve the memory page where this hit exists
        # and make sure it's executable
        code_page = imm.getMemoryPagebyAddress(hit)
        access = code_page.getAccess(human=True)

        if "execute" in access.lower():
            imm.log("[*] Found: %s (0x%08x)" % (search_code, hit), address=hit)

    return "[*] Finished searching for instructions, check the Log window."
# after this !findinstruction <instruction to search for>
# example: !findinstruction mov eax, ebx
# We now have a list of addresses that we can use to get shellcode
# execution—assuming our shellcode starts at ESP