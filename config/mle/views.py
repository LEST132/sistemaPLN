from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from collections import Counter
from PyPDF2 import PdfReader
import string
import os

CORPUS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "media", "textos")

def cargar_corpus(nombre_archivo):
    
    ruta = os.path.join(CORPUS_DIR, nombre_archivo)
    if nombre_archivo.endswith(".txt"):
        with open(ruta, "r", encoding="utf-8") as f:
            return f.read()
    elif nombre_archivo.endswith(".pdf"):
        contenido = ""
        with open(ruta, "rb") as f:
            pdf = PdfReader(f)
            for pagina in pdf.pages:
                contenido += pagina.extract_text() + "\n"
        return contenido
    else:
        return ""


def preprocesar(texto, minusculas=True, quitar_puntuacion=True):

    if minusculas:
        texto = texto.lower()
    if quitar_puntuacion:
        puntuacion_a_eliminar = string.punctuation
        if '@' not in texto:
            puntuacion_a_eliminar = puntuacion_a_eliminar.replace('.', '')
        texto = texto.translate(str.maketrans("", "", puntuacion_a_eliminar))
    return texto.split()


def oraciones_con_fronteras(texto, n):
    oraciones = [o.strip() for o in texto.split('.') if o.strip()]
    resultado = []
    for oracion in oraciones:
        tokens = preprocesar(oracion) 
        resultado.extend(['<s>']*(n-1) + tokens + ['</s>'])
    return resultado



def ngramas(tokens, n):
    return [tuple(tokens[i:i+n]) for i in range(len(tokens)-n+1)]


def autocompletar_view(request):
    sugerencia = ""
    tabla = []
    error = ""
    texto_usuario = ""
    corpus_seleccionado = ""
    corpus_fronteras = []
    ngramas_visualizacion = [] 
    n = int(request.GET.get("n", 2))
    usar_fronteras = request.GET.get("fronteras", "on") == "on"
    
    archivos_corpus = [f for f in os.listdir(CORPUS_DIR) if f.endswith(".txt") or f.endswith(".pdf")]

    if request.method == "POST":
        corpus_seleccionado = request.POST.get("corpus", "")
        texto_usuario = request.POST.get("input_usuario", "")
        n = int(request.POST.get("n", 2))
        usar_fronteras = request.POST.get("fronteras", "on") == "on"

        if not corpus_seleccionado: 
            error = "Debes seleccionar un corpus."
        else:
            texto_corpus = cargar_corpus(corpus_seleccionado)
            corpus_fronteras = corpus_con_fronteras(texto_corpus, n) 
            
            tokens = oraciones_con_fronteras(texto_corpus, n) if usar_fronteras else preprocesar(texto_corpus)
            
            ngramas_visualizacion = ngramas(tokens, n)[:30]
            if n == 1:
                if not tokens:
                    error = "El corpus está vacío o no se pudo leer."
                else:
                    unigram_counts = Counter(ngramas(tokens, 1))
                    total_tokens = len(tokens)
                    candidatos = []
                    for unigram, freq in unigram_counts.items():
                        prob = freq / total_tokens
                        candidatos.append((unigram[0], freq, total_tokens, prob))
                    
                    candidatos.sort(key=lambda x: x[3], reverse=True)
                    tabla = candidatos[:10]
                    if tabla:
                        sugerencia = f"'{tabla[0][0]}' (la palabra más común)"
            else: 
                if not texto_usuario:
                    error = "Debes escribir un texto parcial para predecir."
                else:
                    tokens_usuario = preprocesar(texto_usuario)
                    if len(tokens_usuario) < n - 1:
                        error = f"Debes escribir al menos {n-1} palabra(s) para el contexto."
                    else:
                        contexto = tuple(tokens_usuario[-(n-1):])
                        ngramas_cont = Counter(ngramas(tokens, n))
                        n_1gramas_cont = Counter(ngramas(tokens, n - 1))
                        candidatos = []
                        conteo_contexto = n_1gramas_cont[contexto]
                        if conteo_contexto > 0:
                            for ng, freq in ngramas_cont.items():
                                if ng[:-1] == contexto:
                                    prob = freq / conteo_contexto
                                    candidatos.append((ng[-1], freq, conteo_contexto, prob))
                            
                            candidatos.sort(key=lambda x: x[3], reverse=True)
                            tabla = candidatos[:10]
                            if tabla:
                                sugerencia = tabla[0][0]
                            else:
                                error = "No se encontraron sugerencias para ese contexto."
                        else:
                            error = "El contexto no se encontró en el corpus."

    return render(request, "mle/sig_palabra.html", {
        "archivos_corpus": archivos_corpus,
        "corpus_seleccionado": corpus_seleccionado,
        "n": n,
        "usar_fronteras": usar_fronteras,
        "texto_usuario": texto_usuario,
        "sugerencia": sugerencia,
        "tabla": tabla,
        "error": error,
        "corpus_fronteras": corpus_fronteras,
        "ngramas_visualizacion": ngramas_visualizacion, 
    })


def subir_corpus_view(request):
    mensaje = ""
    if request.method == "POST" and request.FILES.get("archivo"):
        archivo = request.FILES["archivo"]
        if archivo.name.endswith(".txt") or archivo.name.endswith(".pdf"):
            fs = FileSystemStorage(location=CORPUS_DIR)
            fs.save(archivo.name, archivo)
            mensaje = "¡Archivo subido exitosamente!"
        else:
            mensaje = "Solo se permiten archivos .txt o .pdf"
    return render(request, "mle/subir_corpus.html", {"mensaje": mensaje})


def corpus_con_fronteras(texto, n):
    # Divide por punto y agrega n-1 <s> al inicio y </s> al final de cada oración
    oraciones = [o.strip() for o in texto.split('.') if o.strip()]
    resultado = []
    for oracion in oraciones:
        tokens = oracion.split()
        resultado.append(" ".join(['<s>']*(n-1) + tokens + ['</s>']))
    return resultado


def visualizar_fronteras_fijas(texto):
    NUMERO_FRONTERAS_FIJAS = 2
    oraciones = [o.strip() for o in texto.split('.') if o.strip()]
    resultado = []
    for oracion in oraciones:
        tokens = oracion.split()
        resultado.append(" ".join(['<s>'] * NUMERO_FRONTERAS_FIJAS + tokens + ['</s>']))
    return resultado