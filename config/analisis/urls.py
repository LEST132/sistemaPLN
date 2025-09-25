from django.urls import path
from . import views

urlpatterns = [
    path('subir/', views.subir_texto, name='subir_texto'),
    path('', views.lista_textos, name='lista_textos'),
    path('histograma/<int:texto_id>/', views.histograma, name='histograma'),
    path('histograma/<int:texto_id>/<int:n>/', views.histograma, name='histograma_n'),
    path('ngramas/<int:texto_id>/', views.analizar_ngramas, name='analizar_ngramas'),
]
