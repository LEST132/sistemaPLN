from django.shortcuts import render, redirect, get_object_or_404
from .models import TextoAnalizado
from .forms import TextoAnalizadoForm
import matplotlib.pyplot as plt
import io, base64
from collections import Counter
from .preprocesamiento import leer_archivo, limpiar_texto, ngramas

#   subir archivo
def subir_texto(request):
    if request.method == 'POST':
        form = TextoAnalizadoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lista_textos')
    else:
        form = TextoAnalizadoForm()
    return render(request, 'analisis/subir.html', {'form': form})

#   lista de archivos
def lista_textos(request):
    textos = TextoAnalizado.objects.all().order_by('-fecha_subida')
    return render(request, 'analisis/lista.html', {'textos': textos})

#   histograma
def histograma(request, texto_id):
    texto = get_object_or_404(TextoAnalizado, id=texto_id)

    contenido = leer_archivo(texto.archivo.path)

    tokens = limpiar_texto(contenido)

    contador = Counter(tokens)
    histograma = contador.most_common() 

    return render(request, "analisis/histograma.html", {
        "texto": texto,
        "histograma": histograma,
        "tokens": tokens,
    })

#n-gramas
def analizar_ngramas(request, texto_id):
    texto = get_object_or_404(TextoAnalizado, id=texto_id)

    n = int(request.GET.get("n", 1))
    top_k = int(request.GET.get("top_k", 10))

    contenido = leer_archivo(texto.archivo.path)
    tokens = limpiar_texto(contenido)

    total_tokens = len(tokens)
    tipos_tokens = len(set(tokens))

    contador = ngramas(tokens, n)
    ngramas_resuelto = contador.most_common(top_k)

    etiquetas, valores = zip(*ngramas_resuelto) if ngramas_resuelto else ([], [])
    plt.figure(figsize=(10, 5))
    plt.bar(etiquetas, valores, color="skyblue")
    plt.xticks(rotation=45, ha="right")
    plt.title(f"Top {top_k} {n}-gramas en \"{texto.titulo}\"")
    plt.tight_layout()

    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    grafica_png = base64.b64encode(buffer.getvalue()).decode("utf-8")
    buffer.close()

    return render(request, "analisis/ngramas.html", {
        "texto": texto,
        "n": n,
        "top_k": top_k,
        "ngramas": ngramas_resuelto,
        "grafica": grafica_png,
        "total_tokens": total_tokens,
        "tipos_tokens": tipos_tokens,

    })