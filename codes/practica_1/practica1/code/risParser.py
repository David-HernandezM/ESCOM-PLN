from typing import List
import re

RIS_LINE_RE = re.compile(r'^(?P<tag>[A-Z0-9]{2})\s*-\s*(?P<val>.*)$')
RIS_SPLIT_RE = re.compile(r'(?:\r?\n){1,}')  

def parse_ris(text: str) -> List[dict]:
    raw_records = re.split(r'\nER\s*-\s*.*\n?', text.strip(), flags=re.IGNORECASE)
    entries = []
    for raw in raw_records:
        raw = raw.strip()
        if not raw:
            continue
        if not re.search(r'(?m)^TY\s*-\s*', raw):
            continue
        lines = [ln for ln in RIS_SPLIT_RE.split(raw) if ln.strip()]
        fields_multi = {} 
        for ln in lines:
            mm = RIS_LINE_RE.match(ln.strip())
            if not mm:
                continue
            tag = mm.group("tag").upper()
            val = mm.group("val").strip()
            fields_multi.setdefault(tag, []).append(val)
        fields = {k: v[-1] if len(v) == 1 else v for k, v in fields_multi.items()}
        entries.append(fields)
    return entries[0]