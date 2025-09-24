from filereader import readUserFile
from bibParser import parse_bib
from risParser import parse_ris
from bibToRis import bib_to_ris
from risToBib import ris_to_bib
from writeInFile import write_to_file

def main():
    content, isBib = readUserFile()

    if isBib:
        entries = parse_bib(content)
        result = bib_to_ris(entries)
        write_to_file(result, True)
    else:
        entries = parse_ris(content)
        result = ris_to_bib(entries)
        write_to_file(result, False)

    print(f"File created: {"result.ris" if isBib else "result.bib"}")
    

if __name__ == "__main__":
    main()


