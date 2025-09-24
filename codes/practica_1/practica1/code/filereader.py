import argparse
import os
import sys

def readUserFile():
    ap = argparse.ArgumentParser(description="Parser")
    ap.add_argument("input", help="Path to .bib or .ris file")
    args = ap.parse_args()

    filePath = str(args.input)

    if not os.path.exists(filePath):
        print(f"ERROR: File not found: {filePath}", file=sys.stderr)
        sys.exit(1)

    isBib = filePath.endswith(".bib") 
    isRis = filePath.endswith(".ris")

    if not isBib and not isRis:
        print(f"ERROR: Incorrect file with wrong file extension!")
        sys.exit(1)

    with open(filePath, "r", encoding="utf-8") as f:
        content = f.read()
    
    if isBib:
        return (content, True)
    else:
        return (content, False)