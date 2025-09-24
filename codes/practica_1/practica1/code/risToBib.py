import re
from typing import Dict, List, Union, Tuple, Optional

RIS_MAPPING = {
    "AU": "author",
    "TI": "title",
    "PY": "year",
    "VL": "volume",
    "SP": "pages",
    "EP": "pages",
    "DO": "doi",
    "UR": "url",
    "PB": "publisher",
    "JO": "journal",
    "BT": "booktitle",
    "ED": "editor",
    "ET": "edition",
    "KW": "keywords",
    "SN": "issn", 
    "CY": "address",
    "PP": "address",
    "AB": "abstract",
    "ID": "",
    "JOUR": "@article",
    "CONF": "@inproceedings"
}


def _year(s: str) -> str:
    m = re.search(r"\b(\d{4})\b", s or "")
    return m.group(1) if m else (s or "")

def _bib_join_people(values: List[str]) -> str:
    return " and ".join(v.strip() for v in values if v and v.strip())

def _bib_field_line(name: str, value: str) -> str:
    return f"  {name} = {{{value}}},"

def _pages_string(sp: Optional[str], ep: Optional[str]) -> Optional[str]:
    if sp and ep:
        return f"{sp}--{ep}"
    if sp:
        return sp
    return None

def _classify_sn(sn: str) -> str:
    pure = re.sub(r'[^0-9Xx\-]', '', sn or "")
    if re.match(r'^(97[89])[\dXx\-]{10,}$', pure):
        return "isbn"
    if re.match(r'^\d{4}-\d{3}[\dXx]$', pure):
        return "issn"
    return "issn"

def ris_to_bib(rec: Dict[str, Union[str, List[str]]]) -> str:
    def _parse_DA(s: str) -> Tuple[str, str, str]:

        if not s:
            return "", "", ""
        parts = (s or "").split("/")
        parts += [""] * (3 - len(parts)) 
        y_raw, m_raw, d_raw = parts[0].strip(), parts[1].strip(), parts[2].strip()

        yyyy = _year(y_raw)

        def two_digit(x: str, lo: int, hi: int) -> str:
            if not x:
                return ""
            m = re.search(r"\d{1,2}", x)
            if not m:
                return ""
            v = int(m.group(0))
            if lo <= v <= hi:
                return f"{v:02d}"
            return ""

        mm = two_digit(m_raw, 1, 12)
        dd = two_digit(d_raw, 1, 31)
        return yyyy, mm, dd

    ty_code = (rec.get("TY") or "").upper()
    entry_type = RIS_MAPPING.get(ty_code)
    if not entry_type:
        raise ValueError(f"TY no soportado: {ty_code!r}")

    entry_key = (rec.get("ID") or "unnamed")

    ordered_fields: List[str] = []
    fields: Dict[str, str] = {}
    authors: List[str] = []
    editors: List[str] = []
    keywords: List[str] = []
    sp = None
    ep = None
    city = None
    country = None
    isbn_val = None
    issn_val = None

    for tag, value in rec.items():
        if tag in ("TY", "ID"):
            continue

        vals: List[str] = value if isinstance(value, list) else [value]

        if tag == "DA":
            y, m, d = _parse_DA(vals[-1])

            if y and "year" not in fields:
                if "year" not in ordered_fields:
                    ordered_fields.append("year")  
                fields["year"] = _year(y)

            if m:
                if "month" not in ordered_fields:
                    ordered_fields.append("month")
                fields["month"] = m

            if d:
                if "day" not in ordered_fields:
                    ordered_fields.append("day")
                fields["day"] = d
            continue

        bib_field = RIS_MAPPING.get(tag)
        if not bib_field:
            continue

        if tag == "AU":
            if "author" not in ordered_fields:
                ordered_fields.append("author")
            authors.extend(vals)

        elif tag == "ED":
            if "editor" not in ordered_fields:
                ordered_fields.append("editor")
            editors.extend(vals)

        elif tag == "PY":
            if "year" not in ordered_fields:
                ordered_fields.append("year")
            fields["year"] = _year(vals[-1])

        elif tag == "SP":
            if "pages" not in ordered_fields:
                ordered_fields.append("pages")
            sp = vals[-1]

        elif tag == "EP":
            if "pages" not in ordered_fields:
                ordered_fields.append("pages")
            ep = vals[-1]

        elif tag == "KW":
            if "keywords" not in ordered_fields:
                ordered_fields.append("keywords")
            keywords.extend(vals)

        elif tag == "SN":
            for v in vals:
                kind = _classify_sn(v)
                if kind == "isbn":
                    if "isbn" not in ordered_fields:
                        ordered_fields.append("isbn")
                    isbn_val = v
                else:
                    if "issn" not in ordered_fields:
                        ordered_fields.append("issn")
                    issn_val = v

        elif tag in ("CY", "PP"):
            if "address" not in ordered_fields:
                ordered_fields.append("address")
            if tag == "CY":
                city = vals[-1]
            else:
                country = vals[-1]

        else:
            if bib_field not in ordered_fields:
                ordered_fields.append(bib_field)
            fields[bib_field] = vals[-1]

    if authors:
        fields["author"] = _bib_join_people(authors)
    if editors:
        fields["editor"] = _bib_join_people(editors)

    pages_val = _pages_string(sp, ep)
    if pages_val:
        fields["pages"] = pages_val
    else:
        if "pages" in ordered_fields:
            ordered_fields.remove("pages")

    if city or country:
        addr = city if city else ""
        if country:
            addr = f"{addr}, {country}" if addr else country
        fields["address"] = addr
    else:
        if "address" in ordered_fields:
            ordered_fields.remove("address")

    if keywords:
        fields["keywords"] = ", ".join(k.strip() for k in keywords if k.strip())

    if isbn_val:
        fields["isbn"] = isbn_val
    if issn_val:
        fields["issn"] = issn_val

    lines = [f"{entry_type}{{{entry_key},"]

    for name in ordered_fields:
        val = fields.get(name)
        if not val:
            continue
        lines.append(_bib_field_line(name, val))

    if len(lines) > 1 and lines[-1].endswith(","):
        lines[-1] = lines[-1][:-1]

    lines.append("}")
    return "\n".join(lines)







