
def write_to_file(content: str, extIsRis: bool) -> str:
    filename = "result.ris" if extIsRis else "result.bib"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    return filename