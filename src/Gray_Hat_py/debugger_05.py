from binaryninja import *
from binaryninja.enums import SymbolType

# 'bv' is automatically the current BinaryView (loaded file)

def PrintModuleInfo(bv):
    print("Base: 0x%X" % bv.start)
    print("Entry: 0x%X" % bv.entry_point)
    print("Name: %s" % bv.file.filename)
    print("Path: %s" % bv.file.original_filename)
    print("Section count: %d" % len(bv.sections))
    print("Module size: 0x%X" % bv.length)
    
def PrintSectionInfo(section, index):
    print("Section #%d" % (index + 1))
    print("Addr: 0x%X" % section.start)
    print("Name: %s" % section.name)
    print("Size: 0x%X" % section.length)

def PrintImportInfo(sym, bv):
    print("IAT RVA: 0x%X" % (sym.address - bv.start))
    print("IAT VA: 0x%X" % sym.address)
    print("Ordinal: 0x%X" % sym.ordinal if sym.ordinal else "0xFFFFFFFFFFFFFFFF")
    print("Name: %s" % sym.name)
    print("undecoratedName: %s" % sym.raw_name)  # Often empty, like in your output

def main(bv):
    print("Main module information")
    print("-------------------------------------")
    PrintModuleInfo(bv)
    print("Main module section information")
    print("-------------------------------------")
    for i, section in enumerate(bv.sections.values()):
        PrintSectionInfo(section, i)
        print("-------------------------------------")
    
    print("Import information")
    print("-------------------------------------")
    imports = [sym for sym in bv.get_symbols_of_type(SymbolType.ImportAddressSymbol)]
    for sym in imports:
        PrintImportInfo(sym, bv)
        print("")  # Extra line for readability
    
if __name__ == "__main__":
    main(current_view)  # Use 'current_view' if 'bv' isn't auto-available in your version