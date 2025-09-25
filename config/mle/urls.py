from django.urls import path
from . import views

urlpatterns = [
    path('autocompletar/', views.autocompletar_view, name='autocompletar'),
    path('subir_corpus/', views.subir_corpus_view, name='subir_corpus'),
]