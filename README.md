# Proyecto: Autocompletado básico con n-gramas (MLE)
Este proyecto es una aplicación web desarrollada con Django
###### Funcionalidades principales
- Subir corpus (.txt y .pdf) desde la interfaz web.
- Seleccionar corpus para entrenar el modelo.
- Elegir n-grama (unigrama, bigrama, trigrama, hasta n).
- Autocompletar texto: Escribe un contexto y el sistema sugiere la palabra más probable y muestra una tabla con las más probables y sus probabilidades.
- Visualización de n-gramas generados y fronteras de oración.
- Histograma y análisis de textos.

###### ¿Cómo funciona el autocompletado?
- Selección: El usuario elige un corpus y el valor de n (el tamaño del n-grama).
- Contexto: El usuario introduce un texto(contexto). El sistema toma las últimas n-1 palabras como el contexto o historial (h).
- Cálculo: Se buscan los conteos de todos los n-gramas que comienzan con ese contexto.
- Predicción: Se calcula la probabilidad condicional de la siguiente palabra (w) dado el contexto (h) con la fórmula de Estimación de Máxima Verosimilitud (MLE):

			P(w∣h)= C(h) / C(h,w)

- Donde C(h,w) es el conteo del n-grama completo y C(h) es el conteo del contexto. Finalmente, se muestran las palabras más probables.

#### Instalacion

##### Requisitos previos
- Python 3.8+
- Git
- Pipenv (Opcional pero recomendado para gestionar el entorno virtual)

##### Clonar repositorio
		 git clone https://github.com/LEST132/sistemaPLN.git

##### Instalacion de dependencias:
Django, PyPDF2 y NLTK

		 pip install django PyPDF2 nltk

##### Crear y activar entorno virtual(pipenv)
		 pipenv shell

##### Ejecutar el servidor de desarrollo
		python manage.py runserver

##### Estructura del proyecto

```
config/
    manage.py
    settings.py
    urls.py
    ...
analisis/
    views.py
    models.py
    templates/
        analisis/
            lista.html
            ngramas.html
            ...
mle/
    views.py
    templates/
        mle/
            sig_palabra.html
            subir_corpus.html
media/
    textos/
        corpus1.txt
        corpus2.pdf
        ...
```
##### Complementos y recomendaciones

- Puedes agregar más corpus en la carpeta media/textos/ o desde la interfaz web.
- Si usas corpus en PDF,  que sean texto plano (no imágenes).
- Para personalizar el modelo, modifica los parámetros en la interfaz.
