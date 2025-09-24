#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scraper de PubMed Trending (requests + BeautifulSoup) — versión 300 artículos

Cambios clave:
- Recorre páginas /trending/?page=N hasta juntar **300 IDs únicos** (o el valor de --target).
- Extrae IDs desde elementos con atributo "data-ga-label" donde 'href' contenga el mismo valor.
- Para cada ID, descarga https://pubmed.ncbi.nlm.nih.gov/<ID>/?format=pubmed
  y **extrae el contenido del tag <pre>** (texto en formato PubMed).
- Guarda cada artículo en ./out/pubmed_<ID>.txt (solo el texto del <pre>).
- Escribe ./out/summary.csv con pmid, url, status_code, bytes_guardados.
"""

import argparse
import csv
import os
import re
import time
from typing import Iterable, Set, Tuple, List

# import requests
import requests
from bs4 import BeautifulSoup

BASE_TRENDING = "https://pubmed.ncbi.nlm.nih.gov/trending/?page={page}"
BASE_PUBMED_FMT = "https://pubmed.ncbi.nlm.nih.gov/{pmid}/?format=pubmed"

# Un PMID es numérico, pero dejamos alfanum por flexibilidad
PMID_RE = re.compile(r"^/?(?P<id>[A-Za-z0-9]+)(?:/|$)")

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

def extract_ids_from_html(html: str) -> Set[str]:
    """
    Regla: buscar etiquetas con atributo "data-ga-label".
    Si su 'href' contiene lo mismo que "data-ga-label", ese valor es el ID.
    """
    soup = BeautifulSoup(html, "html.parser")
    ids: Set[str] = set()

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
            ids.add(href_id)

    return ids

def crawl_trending_until(session: requests.Session, target: int, delay: float, max_pages: int | None) -> List[str]:
    """
    Recorre /trending/?page=N hasta conseguir 'target' IDs (o hasta max_pages).
    Devuelve lista de IDs en el orden de descubrimiento.
    """
    collected: list[str] = []
    seen: Set[str] = set()

    page = 1
    while len(collected) < target:
        if max_pages is not None and page > max_pages:
            break

        url = BASE_TRENDING.format(page=page)
        resp = session.get(url, timeout=30)
        if resp.status_code == 404:
            # no más páginas
            break
        resp.raise_for_status()

        ids_on_page = extract_ids_from_html(resp.text)
        new = [i for i in ids_on_page if i not in seen]
        for i in new:
            seen.add(i)
            collected.append(i)
            if len(collected) >= target:
                break

        print(f"[Trending p.{page}] encontrados: {len(ids_on_page)} | nuevos: {len(new)} | total: {len(collected)}/{target}")
        page += 1
        time.sleep(delay)

        # Si una página no aportó nada nuevo, y ya vimos varias, podríamos terminar.
        if not new and (max_pages is None):
            # Heurística: si no hay nuevos y no hay límite de páginas, salimos.
            print("[Aviso] No se encontraron nuevos IDs en esta página; deteniendo.")
            break

    return collected

def fetch_pubmed_pre_text(session: requests.Session, pmid: str, delay: float) -> tuple[int, bytes]:
    """
    Descarga ?format=pubmed y retorna (status_code, contenido_bytes_del_<pre>).
    Si no encuentra <pre> pero la respuesta es OK, guarda el body completo.
    """
    url = BASE_PUBMED_FMT.format(pmid=pmid)
    r = session.get(url, timeout=30)
    status = r.status_code

    content = b""
    if r.ok:
        soup = BeautifulSoup(r.text, "html.parser")
        pre = soup.find("pre")
        if pre and pre.get_text(strip=False) is not None:
            content = pre.get_text(strip=False).encode("utf-8", errors="replace")
        else:
            # fallback: guardar todo el HTML (raro que falte <pre>, pero por si acaso)
            content = r.content

    time.sleep(delay)
    return status, content

def main():
    p = argparse.ArgumentParser(description="Scraper PubMed Trending — 300 artículos con <pre> (requests + bs4).")
    p.add_argument("--target", type=int, default=300, help="Cantidad de artículos a recolectar (IDs únicos).")
    p.add_argument("--delay", type=float, default=0.7, help="Pausa (seg) entre requests.")
    p.add_argument("--out", type=str, default="out", help="Directorio de salida.")
    p.add_argument("--max-pages", type=int, default=None, help="Máximo de páginas trending a recorrer (opcional).")
    args = p.parse_args()

    os.makedirs(args.out, exist_ok=True)
    session = build_session()

    # 1) Recolectar IDs hasta 'target'
    ids = crawl_trending_until(session, args.target, args.delay, args.max_pages)
    print(f"\nTotal IDs recolectados: {len(ids)} (objetivo: {args.target})")

    # 2) Por cada ID, descargar ?format=pubmed y extraer el <pre>
    summary_csv = os.path.join(args.out, "summary.csv")
    with open(summary_csv, "w", newline="", encoding="utf-8") as fcsv:
        writer = csv.writer(fcsv)
        writer.writerow(["pmid", "url", "status_code", "bytes_saved", "note"])

        for idx, pmid in enumerate(ids, 1):
            url = BASE_PUBMED_FMT.format(pmid=pmid)
            try:
                status, pre_bytes = fetch_pubmed_pre_text(session, pmid, args.delay)
                out_path = os.path.join(args.out, f"pubmed_{pmid}.txt")
                saved = 0
                note = ""
                if status == 200 and pre_bytes:
                    with open(out_path, "wb") as f:
                        f.write(pre_bytes)
                    saved = len(pre_bytes)
                elif status == 200 and not pre_bytes:
                    note = "Sin <pre>, no se guardó contenido."
                else:
                    note = f"HTTP {status}"

                writer.writerow([pmid, url, status, saved, note])
                print(f"[{idx}/{len(ids)}] {pmid} -> {status}, bytes={saved}{' ('+note+')' if note else ''}")
            except Exception as e:
                writer.writerow([pmid, url, 0, 0, f"Error: {e}"])
                print(f"[{idx}/{len(ids)}] {pmid} -> Error: {e}")

    print(f"\nListo. Archivos en: {os.path.abspath(args.out)}")
    print(f"Resumen CSV: {summary_csv}")

if __name__ == "__main__":
    main()
