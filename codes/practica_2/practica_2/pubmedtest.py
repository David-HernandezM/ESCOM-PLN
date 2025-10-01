import csv
import re
import time
from typing import Dict, List, Optional, Set

import requests
from bs4 import BeautifulSoup

# -------------------- Config --------------------
TARGET_ROWS = 300
DELAY_BETWEEN_REQUESTS = 0.1  # segundos
MAX_PAGES = None              # None = sin límite; o un int si quieres tope
OUT_CSV = "pubmed_extracted.csv"

BASE_TRENDING = "https://pubmed.ncbi.nlm.nih.gov/trending/?page={page}"
BASE_PUBMED_FMT = "https://pubmed.ncbi.nlm.nih.gov/{pmid}/?format=pubmed"

PMID_RE = re.compile(r"^/?(?P<id>[A-Za-z0-9]+)(?:/|$)")

# -------------------- Parsers MEDLINE --------------------
TAG_RE = re.compile(r"^([A-Z]{2,4})\s*-\s(.*)$")

# DOI robusto (Crossref-like)
DOI_RE_STRICT = re.compile(r"(10\.\d{4,9}/[-._;()/:A-Z0-9]+)", re.I)

# DOI que esté explícitamente marcado con [doi] EN LID
# Captura hasta antes de espacio o '[' para evitar truncados
DOI_IN_LID_WITH_DOI_TAG = re.compile(r"(10\.\d{4,9}/[^\s\[\]]+)\s*\[doi\]", re.I)

DATE_RE = re.compile(
    r"(?P<year>\d{4})"
    r"(?:\s+(?P<mon>[A-Za-z]{3,9}))?"
    r"(?:\s+(?P<day>\d{1,2}))?"
)

MONTHS = {
    'jan': 1, 'january': 1,
    'feb': 2, 'february': 2,
    'mar': 3, 'march': 3,
    'apr': 4, 'april': 4,
    'may': 5,
    'jun': 6, 'june': 6,
    'jul': 7, 'july': 7,
    'aug': 8, 'august': 8,
    'sep': 9, 'sept': 9, 'september': 9,
    'oct': 10, 'october': 10,
    'nov': 11, 'november': 11,
    'dec': 12, 'december': 12,
}

def build_session() -> requests.Session:
    s = requests.Session()
    s.headers.update({
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "es-MX,es;q=0.9,en;q=0.8",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    })
    return s

def normalize_space(s: str) -> str:
    return re.sub(r"\s+", " ", s.strip())

def parse_medline_text(text: str) -> Dict[str, List[str]]:
    data: Dict[str, List[str]] = {}
    current_tag: Optional[str] = None
    for raw in text.splitlines():
        line = raw.rstrip("\n")
        m = TAG_RE.match(line)
        if m:
            tag, content = m.group(1), m.group(2)
            current_tag = tag
            data.setdefault(tag, []).append(content)
        else:
            if current_tag and (line.startswith(" ") or line.startswith("\t")):
                if data[current_tag]:
                    data[current_tag][-1] += "\n" + line.strip()
            else:
                current_tag = None
    return data

def clean_doi_tail(s: str) -> str:
    # Quita colas típicas
    return s.rstrip(").,;]")

def pick_doi_from_LID(lids: List[str]) -> Optional[str]:
    """
    1) Buscar DOI en LID que esté explícitamente seguido de [doi].
    2) Si no hay, buscar todos los DOI dentro de LID y devolver el más largo.
    """
    # Paso 1: estrictamente LID ... [doi]
    for lid in lids:
        m = DOI_IN_LID_WITH_DOI_TAG.search(lid)
        if m:
            return clean_doi_tail(m.group(1))

    # Paso 2: fallback: DOI más largo encontrado en LID
    best = None
    best_len = -1
    for lid in lids:
        for c in DOI_RE_STRICT.findall(lid):
            c = clean_doi_tail(c)
            if len(c) > best_len:
                best = c
                best_len = len(c)
    return best

def join_multiline(values: List[str]) -> str:
    joined = " ".join(normalize_space(v.replace("\n", " ")) for v in values)
    return normalize_space(joined)

def parse_date_dp(dp_values: List[str]) -> Optional[str]:
    raw = " ".join(dp_values).replace(";", " ")
    m = DATE_RE.search(raw)
    if not m:
        return None
    year = int(m.group("year"))
    mon_txt = m.group("mon")
    day_txt = m.group("day")
    mon = MONTHS.get(mon_txt.strip().lower(), 1) if mon_txt else 1
    if day_txt:
        day_txt = day_txt.split("-")[0]
        day = int(day_txt)
    else:
        day = 1
    return f"{day:02d}/{mon:02d}/{year:04d}"

def extract_required_fields(m: Dict[str, List[str]]) -> Optional[Dict[str, str]]:
    doi = pick_doi_from_LID(m.get("LID", []))
    title = join_multiline(m.get("TI", [])) if "TI" in m else None

    # Autores separados por coma
    authors_list = m.get("AU", [])
    authors = ", ".join(normalize_space(a) for a in authors_list) if authors_list else None

    abstract = join_multiline(m.get("AB", [])) if "AB" in m else None
    journal = join_multiline(m.get("JT", [])) if "JT" in m else None
    date = parse_date_dp(m.get("DP", [])) if "DP" in m else None

    fields = {
        "DOI": doi,
        "Title": title,
        "Authors": authors,
        "Abstract": abstract,
        "Journal": journal,
        "Date": date,
    }
    return fields if all(fields.values()) else None

# -------------------- Descarga por página --------------------

def extract_ids_from_html(html: str) -> List[str]:
    soup = BeautifulSoup(html, "html.parser")
    ids: List[str] = []
    for tag in soup.find_all(attrs={"data-ga-label": True}):
        ga = (tag.get("data-ga-label") or "").strip()
        href = (tag.get("href") or "").strip()
        if not ga or not href:
            continue
        m = PMID_RE.match(href.lstrip("/"))
        if not m:
            continue
        href_id = m.group("id")
        if ga == href_id:
            ids.append(href_id)
    return ids

def fetch_pubmed_pre_text(session: requests.Session, pmid: str) -> Optional[str]:
    url = BASE_PUBMED_FMT.format(pmid=pmid)
    r = session.get(url, timeout=30)
    if not r.ok:
        return None
    soup = BeautifulSoup(r.text, "html.parser")
    pre = soup.find("pre")
    if pre and pre.get_text(strip=False) is not None:
        return pre.get_text(strip=False)
    # último recurso: html completo
    return r.text

def process_trending_stream_to_csv():
    session = build_session()
    seen: Set[str] = set()
    written = 0
    page = 1

    with open(OUT_CSV, "w", newline="", encoding="utf-8") as fcsv:
        writer = csv.writer(fcsv)
        writer.writerow(["DOI", "Title", "Authors", "Abstract", "Journal", "Date"])

        while written < TARGET_ROWS:
            if MAX_PAGES is not None and page > MAX_PAGES:
                print(f"[FIN] MAX_PAGES={MAX_PAGES} sin llegar a {TARGET_ROWS}.")
                break

            url = BASE_TRENDING.format(page=page)
            resp = session.get(url, timeout=30)
            if resp.status_code == 404:
                print("[FIN] No hay más páginas de trending.")
                break
            resp.raise_for_status()

            pmids = extract_ids_from_html(resp.text)
            new_pmids = [pid for pid in pmids if pid not in seen]
            for pid in new_pmids:
                seen.add(pid)
                pre_text = fetch_pubmed_pre_text(session, pid)
                time.sleep(DELAY_BETWEEN_REQUESTS)
                if not pre_text:
                    continue

                med = parse_medline_text(pre_text)
                fields = extract_required_fields(med)
                if fields:
                    writer.writerow([
                        fields["DOI"],
                        fields["Title"],
                        fields["Authors"],
                        fields["Abstract"],
                        fields["Journal"],
                        fields["Date"],
                    ])
                    written += 1
                    print(f"[p.{page}] +1 ({written}/{TARGET_ROWS})  PMID={pid}")
                    if written >= TARGET_ROWS:
                        break

            print(f"[Trending p.{page}] nuevos={len(new_pmids)} | válidos acumulados={written}")
            page += 1

    if written < TARGET_ROWS:
        print(f"[AVISO] Solo se escribieron {written} artículos válidos (requeridos {TARGET_ROWS}).")
    else:
        print(f"[OK] CSV con {written} artículos: {OUT_CSV}")

if __name__ == "__main__":
    process_trending_stream_to_csv()
