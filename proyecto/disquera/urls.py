from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('artistas', views.artistas, name='artistas'),
    path('artistas/contratos', views.contratos, name='contratos'),
    path('artistas/regalias', views.regalias, name='regalias'),
    path('catalogo', views.catalogo, name='catalogo'),
    path('catalogo/inspeccion', views.inspeccionAlbum, name='inspeccionAlbum'),
    path('ventas', views.ventas, name='ventas'),
]