from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
from django.contrib import messages

from .models import Prueba
# Create your views here.

def inicio(request):
    return render(request, 'paginas/index.html')

def artistas(request):
    if request.method == 'POST':
        nombre_artista = request.POST.get('nombre_artista')

        # Execute SQL query using Django's raw SQL API
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM artista WHERE nombre_artista LIKE %s', ['%{}%'.format(nombre_artista)])
            encontrados = cursor.fetchall()

        if not encontrados:
            # No artists found, send a message
            messages.info(request, 'No se encontraron artistas con ese nombre.')

        return render(request, 'paginas/artistas.html', {'artistas': encontrados})
    else:
        sql = """SELECT * FROM artista;"""
        with connection.cursor() as cursor:
            cursor.execute(sql)
            artistasPrueba = cursor.fetchall()
        
        '''artistasPrueba = Prueba.objects.all()'''
        
        return render(request, 'paginas/artistas.html', {'artistas': artistasPrueba})
    
def catalogo(request):
    formatted_albums = []
    if request.method == 'POST':
        artista = request.POST['artista']
        generoPost = request.POST['genero']
        precioMin = request.POST['precioMinimo']
        precioMax = request.POST['precioMaximo']
        
         # Prepare placeholders and values
        placeholders = [
            "ar.nombre_artista LIKE %s",
            "g.descripcion LIKE %s",
            "a.precio >= %s",
            "a.precio <= %s",
        ]
        values = [
            (f"%{artista}%",),
            (f"%{generoPost}%",),
            (precioMin,),
            (precioMax,),
        ]

        sql = f"""SELECT a.titulo, ar.nombre_artista, a.fecha_lanzamiento, a.precio, a.edicion_especial, g.descripcion FROM album a JOIN artista ar ON a.id_artista = ar.id_artista JOIN genero g ON a.id_genero = g.id_genero WHERE {' AND '.join(placeholders)} ORDER BY a.titulo;"""

        with connection.cursor() as cursor:
            cursor.execute(sql, values)
            albums = cursor.fetchall()

        for album in albums:
            release_date = album[2]
            formatted_date = release_date.strftime('%m-%d-%Y')
            price = album[3]
            especial = 'Especial' if album[4] == 1 else 'Normal'
            formatted_price = f"{price:.2f}"
            formatted_album = (album[0], album[1], formatted_date, formatted_price, especial, album[5])
            formatted_albums.append(formatted_album)
        
    sql = """SELECT nombre_artista FROM artista;"""
    with connection.cursor() as cursor:
        cursor.execute(sql)
        nombres = cursor.fetchall()
    opciones_nombres = [
        ('','Todos'),
    ]
    for nombre in nombres:
        option_value = nombre[0]  # Extract artist name from tuple
        option_text = (option_value, option_value)
        opciones_nombres.append(option_text)

    sql = """SELECT descripcion FROM genero;"""
    with connection.cursor() as cursor:
        cursor.execute(sql)
        generos = cursor.fetchall()
    opciones_generos = [
        ('','Todos'),
    ]
    for genero in generos:
        option_value = genero[0]
        option_text = (option_value, option_value)
        opciones_generos.append(option_text)

    return render(request, 'paginas/catalogo.html', {'nombres': opciones_nombres, 'generos': opciones_generos, 'albums': formatted_albums})