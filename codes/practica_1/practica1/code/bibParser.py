from typing import List
import re

ENTRY_RE = re.compile(
    r'@(?P<etype>[A-Za-z]+)\s*{\s*(?P<key>[^,]+)\s*,(?P<body>.*?)^\s*}\s*',
    flags=re.DOTALL | re.IGNORECASE | re.MULTILINE
)

FIELD_RE = re.compile(
    r'(?P<name>[A-Za-z][\w-]*)\s*=\s*(?P<val>('
    r'"[^"]*"|'
    r'\{(?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*\}'
    r'))\s*,?',
    flags=re.DOTALL | re.IGNORECASE
)

def _strip_braces_quotes(s: str) -> str:
    s = s.strip()
    if s.startswith("{") and s.endswith("}"):
        return s[1:-1].strip()
    if s.startswith('"') and s.endswith('"'):
        return s[1:-1].strip()
    return s

def parse_bib(text: str) -> List[dict]:
    entries = []
    for m in ENTRY_RE.finditer(text):
        etype = m.group("etype").strip()
        key = m.group("key").strip()
        body = m.group("body")
        fields = {}
        for fm in FIELD_RE.finditer(body):
            name = fm.group("name").strip().lower()
            val = _strip_braces_quotes(fm.group("val"))
            fields[name] = val
        entries.append({"type": f"@{etype.lower()}", "id": key, "fields": fields})
    return entries[0]