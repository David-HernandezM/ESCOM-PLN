#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import sys
# import pandas as pd


# import web_scrapping as ws
# import normalization_spacy_english as norm_spacy
# import normalization_nltk_english as norm_nltk
# import vectorizacion as vect
# import document_similarity as sim

# # ------------------ COMANDOS ------------------

# def cmd_collect(args):
#     """
#     Usa el script de web_scrapping para recolectar artículos.
#     Aquí deberías implementar la lógica de guardar en CSV
#     con las columnas DOI, Title, Authors, Abstract, Section, Date.
#     """
#     print("[INFO] Recolectando artículos de arXiv (ejemplo)")
#     df = ws.scrape_arxiv(sections=["cs.CL","cs.CV","cs.CR"], per_section=100)  # ajustar
#     df.to_csv(args.output, sep="\t", index=False)
#     print(f"[OK] Corpus crudo guardado en {args.output}")

# def cmd_normalize(args):
#     """
#     Normaliza títulos y abstracts usando spaCy o NLTK.
#     """
#     df = pd.read_csv(args.input, sep="\t")
#     if args.engine == "spacy":
#         df["Title"] = norm_spacy.normalize_series(df["Title"])
#         df["Abstract"] = norm_spacy.normalize_series(df["Abstract"])
#     else:
#         df["Title"] = norm_nltk.normalize_series(df["Title"])
#         df["Abstract"] = norm_nltk.normalize_series(df["Abstract"])
#     df.to_csv(args.output, sep="\t", index=False)
#     print(f"[OK] Corpus normalizado guardado en {args.output}")

# def cmd_vectorize(args):
#     """
#     Genera representaciones vectoriales (freq, bin, tfidf).
#     """
#     df = pd.read_csv(args.input, sep="\t")
#     vect.build_and_save_models(
#         df=df,
#         repo=args.repo,
#         models_dir=args.models,
#         field=args.field,
#         ngram=args.ngram,
#         repr_kind=args.repr
#     )
#     print(f"[OK] Modelos vectoriales guardados en {args.models}")

# def cmd_retrieve(args):
#     """
#     Recupera artículos similares usando cosine similarity.
#     """
#     results = sim.retrieve_similar(
#         query_text=args.query_text,
#         repo=args.repo,
#         field=args.field,
#         ngram=args.ngram,
#         repr_kind=args.repr,
#         models_dir=args.models,
#         engine=args.engine,
#         top=args.top
#     )
#     print("\nTop similares:")
#     for rank, (doc_id, score) in enumerate(results, 1):
#         print(f"{rank}. {doc_id}\t{score:.4f}")

# ------------------ PARSER ------------------

def build_parser():
    p = argparse.ArgumentParser(prog="dsim", description="Practice II - Document similarity (CLI)")
    sub = p.add_subparsers(dest="cmd", required=True)

    # collect
    c = sub.add_parser("collect", help="Recolección de artículos")
    c.add_argument("--output", default="data/arxiv_raw_corpus.csv")
    # c.set_defaults(func=cmd_collect)

    # # normalize
    # n = sub.add_parser("normalize", help="Normalización de texto")
    # n.add_argument("--engine", choices=["spacy","nltk"], default="spacy")
    # n.add_argument("--input", required=True)
    # n.add_argument("--output", required=True)
    # n.set_defaults(func=cmd_normalize)

    # # vectorize
    # v = sub.add_parser("vectorize", help="Vectorización de corpus")
    # v.add_argument("--repo", default="arxiv")
    # v.add_argument("--field", choices=["title","abstract","both"], default="both")
    # v.add_argument("--ngram", choices=["uni","bi"], default="uni")
    # v.add_argument("--repr", choices=["freq","bin","tfidf"], default="tfidf")
    # v.add_argument("--input", required=True)
    # v.add_argument("--models", default="models/arxiv")
    # v.set_defaults(func=cmd_vectorize)

    # # retrieve
    # r = sub.add_parser("retrieve", help="Recuperación de similares")
    # r.add_argument("--repo", default="arxiv")
    # r.add_argument("--field", choices=["title","abstract"], default="title")
    # r.add_argument("--ngram", choices=["uni","bi"], default="uni")
    # r.add_argument("--repr", choices=["freq","bin","tfidf"], default="tfidf")
    # r.add_argument("--engine", choices=["spacy","nltk"], default="spacy")
    # r.add_argument("--models", default="models/arxiv")
    # r.add_argument("--query-text", required=True)
    # r.add_argument("--top", type=int, default=10)
    # r.set_defaults(func=cmd_retrieve)

    return p

def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)

if __name__ == "__main__":
    sys.exit(main())
