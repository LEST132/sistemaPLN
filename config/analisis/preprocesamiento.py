import string
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords', quiet=True)

stopwords_es = set(stopwords.words('spanish'))
puntuacion = set(string.punctuation)

def limpiar_texto(texto):

    texto = texto.lower()

    texto = "".join([c if c not in puntuacion else " " for c in texto])

    tokens = texto.split()

    tokens_limpios = [t for t in tokens if t not in stopwords_es]

    return tokens_limpios
