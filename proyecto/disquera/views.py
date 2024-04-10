from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection

from .models import Prueba
# Create your views here.

def inicio(request):
    return render(request, 'paginas/index.html')

def artistas(request):
    
    sql = """SELECT * FROM Prueba;"""
    with connection.cursor() as cursor:
        cursor.execute(sql)
        artistasPrueba = cursor.fetchall()
    
    '''artistasPrueba = Prueba.objects.all()'''
    
    return render(request, 'paginas/artistas.html', {'artistas': artistasPrueba})