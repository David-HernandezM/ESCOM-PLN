from typing import List, Tuple, Optional
import re

RIS_MAPPING = {
    "author": "AU",
    "title": "TI",
    "year": "PY",
    "volume": "VL",
    "number": "IS",
    "pages": ["SP","EP"],
    "doi": "DO",
    "url": "UR",
    "publisher": "PB",
    "journal": "JO",
    "booktitle": "BT",
    "editor": "ED",
    "edition": "ET",
    "keywords": "KW",
    "issn": "SN",
    "isbn": "SN",
    "address": ["CY", "PP"],
    "abstract": "AB",
    "@article": "JOUR",
    "@inproceedings": "CONF",
}

def _split_persons_bib(value: str) -> List[str]:
    return [p.strip() for p in re.split(r"\s+and\s+", value or "") if p.strip()]

def _pages_to_sp_ep(pages: str) -> Tuple[Optional[str], Optional[str]]:
    m = re.match(r"^\s*(\d+)\s*[-–—]{1,2}\s*(\d+)\s*$", pages or "")
    if m:
        return m.group(1), m.group(2)
    pages = (pages or "").strip()
    return (pages if pages else None), None

def _pick_year(text: str) -> str:
    m = re.search(r"\b(\d{4})\b", text or "")
    return m.group(1) if m else ""

def _norm_month(mm: str) -> str:
    if not mm:
        return ""
    s = str(mm).strip().lower()
    s = re.sub(r"[.\s{}\\']", "", s)  

    mdig = re.search(r"\d{1,2}", s)
    if mdig:
        m = int(mdig.group(0))
        if 1 <= m <= 12:
            return f"{m:02d}"
        
    table = {
        "jan":1,"january":1,"ene":1,"enero":1,
        "feb":2,"february":2,"febrero":2,
        "mar":3,"march":3,"marzo":3,
        "apr":4,"april":4,"abr":4,"abril":4,
        "may":5,"mayo":5,
        "jun":6,"june":6,"junio":6,
        "jul":7,"july":7,"julio":7,
        "aug":8,"august":8,"ago":8,"agosto":8,
        "sep":9,"sept":9,"september":9,"septiembre":9,
        "oct":10,"october":10,"octubre":10,
        "nov":11,"november":11,"noviembre":11,
        "dec":12,"december":12,"dic":12,"diciembre":12,
    }

    if s in table:
        return f"{table[s]:02d}"
    return ""

def _norm_day(dd: str) -> str:
    if not dd:
        return ""
    dig = re.search(r"\d{1,2}", str(dd))
    if not dig:
        return ""
    d = int(dig.group(0))
    if 1 <= d <= 31:
        return f"{d:02d}"
    return ""

def _format_tag(tag: str, value: str) -> str:
    return f"{tag:2}  - {value}"

def _split_city_country(addr: str) -> Tuple[Optional[str], Optional[str]]:
    if not addr:
        return None, None
    parts = [p.strip() for p in addr.split(",") if p.strip()]
    if len(parts) >= 2:
        return parts[0], ", ".join(parts[1:])
    return addr.strip(), None

def bib_to_ris(entry: dict) -> str:
    etype = (entry.get("type") or "").lower()
    tag = RIS_MAPPING.get(etype)
    if not tag:
        raise ValueError(f"Unsupported BibTeX type: {etype}")

    key = (entry.get("id") or "").strip()
    f = entry.get("fields", {}) or {}
    lines: List[str] = []

    lines.append(_format_tag("TY", tag))

    tag = RIS_MAPPING.get("author")
    if tag and f.get("author"):
        for person in _split_persons_bib(f["author"]):
            lines.append(_format_tag(tag, person))

    tag = RIS_MAPPING.get("editor")
    if tag and f.get("editor"):
        for person in _split_persons_bib(f["editor"]):
            lines.append(_format_tag(tag, person))

    year_raw = f.get("year")
    month_raw = f.get("month")
    day_raw = f.get("day")

    yyyy = _pick_year(year_raw or "")
    mm = _norm_month(month_raw) if month_raw else ""
    dd = _norm_day(day_raw) if day_raw else ""

    tag = RIS_MAPPING.get("year")
    if tag and yyyy:
        lines.append(_format_tag(tag, yyyy))

    if any([yyyy, mm, dd]):
        da = "/".join([yyyy, mm, dd])
        lines.append(_format_tag("DA", da))

    tag = RIS_MAPPING.get("title")
    if tag and f.get("title"):
        lines.append(_format_tag(tag, f["title"].strip()))

    tag = RIS_MAPPING.get("journal")
    if tag and f.get("journal"):
        lines.append(_format_tag(tag, f["journal"].strip()))
    tag = RIS_MAPPING.get("booktitle")
    if tag and f.get("booktitle"):
        lines.append(_format_tag(tag, f["booktitle"].strip()))

    tag = RIS_MAPPING.get("volume")
    if tag and f.get("volume"):
        lines.append(_format_tag(tag, f["volume"].strip()))
    tag = RIS_MAPPING.get("number")
    if tag and f.get("number"):
        lines.append(_format_tag(tag, f["number"].strip()))

    tags_pages = RIS_MAPPING.get("pages")
    if tags_pages and f.get("pages"):
        tags = [tags_pages] if isinstance(tags_pages, str) else list(tags_pages)
        sp_tag = tags[0] if len(tags) >= 1 else None
        ep_tag = tags[1] if len(tags) >= 2 else None
        sp, ep = _pages_to_sp_ep(f["pages"])
        if sp_tag and sp:
            lines.append(_format_tag(sp_tag, sp))
        if ep_tag and ep:
            lines.append(_format_tag(ep_tag, ep))

    tag = RIS_MAPPING.get("publisher")
    if tag and f.get("publisher"):
        lines.append(_format_tag(tag, f["publisher"].strip()))

    tags_addr = RIS_MAPPING.get("address")
    if tags_addr and f.get("address"):
        tags = [tags_addr] if isinstance(tags_addr, str) else list(tags_addr)
        cy_tag = tags[0] if len(tags) >= 1 else None
        pp_tag = tags[1] if len(tags) >= 2 else None
        city, country = _split_city_country(f["address"])
        if cy_tag and city:
            lines.append(_format_tag(cy_tag, city))
        if pp_tag and country:
            lines.append(_format_tag(pp_tag, country))

    tag = RIS_MAPPING.get("edition")
    if tag and f.get("edition"):
        lines.append(_format_tag(tag, f["edition"].strip()))

    tag = RIS_MAPPING.get("abstract")
    if tag and f.get("abstract"):
        lines.append(_format_tag(tag, f["abstract"].strip()))

    tag = RIS_MAPPING.get("doi")
    if tag and f.get("doi"):
        lines.append(_format_tag(tag, f["doi"].strip()))
    tag = RIS_MAPPING.get("url")
    if tag and f.get("url"):
        lines.append(_format_tag(tag, f["url"].strip()))

    tag = RIS_MAPPING.get("keywords")
    if tag and f.get("keywords"):
        for kw in [k.strip() for k in re.split(r",\s*", f["keywords"]) if k.strip()]:
            lines.append(_format_tag(tag, kw))

    tag = RIS_MAPPING.get("issn")
    if tag and f.get("issn"):
        lines.append(_format_tag(tag, f["issn"].strip()))
    tag = RIS_MAPPING.get("isbn")
    if tag and f.get("isbn"):
        lines.append(_format_tag(tag, f["isbn"].strip()))

    if key:
        lines.append(_format_tag("ID", key))

    lines.append(_format_tag("ER", ""))

    return "\n".join(lines)


