import string
from nltk.corpus import stopwords
from PyPDF2 import PdfReader
from collections import Counter

STOPWORDS = set(stopwords.words('spanish'))

def leer_archivo(ruta):

    if ruta.endswith(".txt"):
        with open(ruta, "r", encoding="utf-8") as f:
            return f.read()
    elif ruta.endswith(".pdf"):
        contenido = ""
        with open(ruta, "rb") as f:
            pdf = PdfReader(f)
            for pagina in pdf.pages:
                contenido += pagina.extract_text() + "\n"
        return contenido
    else:
        raise ValueError("Formato de archivo no soportado")

def limpiar_texto(texto):

    texto = texto.lower()

    texto = texto.translate(str.maketrans("", "", string.punctuation))

    tokens = texto.split()

    tokens_limpios = []
    for i in tokens:
        if i not in STOPWORDS:
            tokens_limpios.append(i)

    return tokens_limpios

def ngramas(tokens, n=1):
    ngramas_encontrados = []

    for i in range(len(tokens) - n + 1):
        ngrama_temporal = tokens[i:i+n]
        ngrama_unido = " ".join(ngrama_temporal)
        ngramas_encontrados.append(ngrama_unido)

    return Counter(ngramas_encontrados)
