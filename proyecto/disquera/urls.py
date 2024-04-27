from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('artistas', views.artistas, name='artistas'),
    path('catalogo', views.catalogo, name='catalogo'),
]