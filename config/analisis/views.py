from django.shortcuts import render, redirect, get_object_or_404
from .forms import TextoAnalizadoForm
from .models import TextoAnalizado
from collections import Counter

# Vista: subir archivo
def subir_texto(request):
    if request.method == 'POST':
        form = TextoAnalizadoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lista_textos')
    else:
        form = TextoAnalizadoForm()
    return render(request, 'analisis/subir.html', {'form': form})

# Vista: lista de archivos subidos
def lista_textos(request):
    textos = TextoAnalizado.objects.all().order_by('-fecha_subida')
    return render(request, 'analisis/lista.html', {'textos': textos})

# Vista: generar histograma de palabras
def histograma(request, texto_id):
    texto = get_object_or_404(TextoAnalizado, id=texto_id)
    contenido = ""
    with open(texto.archivo.path, "r", encoding="utf-8") as f:
        contenido = f.read()

    palabras = contenido.split()
    contador = Counter(palabras)
    histograma = contador.most_common(20)  # top 20 palabras más frecuentes

    return render(request, 'analisis/histograma.html', {
        'texto': texto,
        'histograma': histograma
    })
