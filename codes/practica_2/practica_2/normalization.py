import pandas as pd
import spacy

# Cargar modelo spaCy inglés
nlp = spacy.load("en_core_web_sm")

# Función de normalización
def normalize_text(text):
    if pd.isna(text):
        return ""
    doc = nlp(text.lower())
    tokens = []
    for token in doc:
        # Filtrar por POS (descartar artículos, preposiciones, conjunciones, pronombres)
        if token.pos_ in ["DET", "ADP", "CCONJ", "PRON"]:
            continue
        # Lematizar y guardar
        tokens.append(token.lemma_)
    return " ".join(tokens)

# Leer CSV crudo
df = pd.read_csv("arxiv_raw_corpus.csv")

# Normalizar columnas Title y Abstract
df["title"] = df["title"].apply(normalize_text)
df["abstract"] = df["abstract"].apply(normalize_text)

# Guardar CSV normalizado
df.to_csv("arxiv_normalized_corpus.csv", index=False)

print("Corpus normalizado guardado en arxiv_normalized_corpus.csv")
