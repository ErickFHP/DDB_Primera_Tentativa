from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
from django.db import connections
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

        '''sql = """SELECT * FROM tarea;"""
        with connections['prueba'].cursor() as cursor:
            cursor.execute(sql)
            resultado = cursor.fetchall()

        print(resultado)'''
        
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
            formatted_date = release_date.strftime('%d-%m-%Y')
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

def contratos(request):
    resultadosAm = []
    resultadosEu = []
    resultadosAo = []
    if request.method == 'POST':
        inicio = request.POST['fecha-inicio']
        final = request.POST['fecha-fin']
        artista = request.POST['artista']
        continente = request.POST['continente']

        # Prepare placeholders and values
        placeholders = [
            "c.fecha_inicio >= %s",
            "c.fecha_fin <= %s",
            "a.nombre_artista LIKE %s",
        ]
        values = [
            (inicio,),
            (final,),
            (f"%{artista}%",),
        ]

        if continente == 'America' or continente == '':
            sql = f"""SELECT c.id_contrato, c.fecha_inicio, c.fecha_fin, a.nombre_artista AS artista, s.nombre AS sede 
                FROM contrato_america c 
                JOIN artista a ON c.id_artista = a.id_artista 
                JOIN sede s ON c.id_sede = s.id_sede 
                WHERE {' AND '.join(placeholders)} 
                ORDER BY c.fecha_inicio ASC;"""
            with connection.cursor() as cursor:
                cursor.execute(sql, values)
                america = cursor.fetchall()
            
            for res in america:
                resultadosAm.append([res[0], res[1].strftime('%d-%m-%Y'), res[2].strftime('%d-%m-%Y'), res[3], res[4], 'América'])

        if continente == 'Europa' or continente == '':
            sql = f"""SELECT c.id_contrato, c.fecha_inicio, c.fecha_fin, a.nombre_artista AS artista, s.nombre AS sede 
                FROM contrato_europa c 
                JOIN artista a ON c.id_artista = a.id_artista 
                JOIN sede s ON c.id_sede = s.id_sede 
                WHERE {' AND '.join(placeholders)} 
                ORDER BY c.fecha_inicio ASC;"""
            with connection.cursor() as cursor:
                cursor.execute(sql, values)
                europa = cursor.fetchall()
            
            for res in europa:
                resultadosEu.append([res[0], res[1].strftime('%d-%m-%Y'), res[2].strftime('%d-%m-%Y'), res[3], res[4], 'Europa'])

        if continente == 'Asia/Oceania' or continente == '':
            sql = f"""SELECT c.id_contrato, c.fecha_inicio, c.fecha_fin, a.nombre_artista AS artista, s.nombre AS sede 
                FROM contrato_asiaoceania c 
                JOIN artista a ON c.id_artista = a.id_artista 
                JOIN sede s ON c.id_sede = s.id_sede 
                WHERE {' AND '.join(placeholders)} 
                ORDER BY c.fecha_inicio ASC;"""
            with connection.cursor() as cursor:
                cursor.execute(sql, values)
                asia = cursor.fetchall()
            
            for res in asia:
                resultadosAo.append([res[0], res[1].strftime('%d-%m-%Y'), res[2].strftime('%d-%m-%Y'), res[3], res[4], 'Asia/Oceania'])

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

    return render(request, 'paginas/contratos.html',{'nombres': opciones_nombres, 'america': resultadosAm, 'europa': resultadosEu, 'asia': resultadosAo})

def regalias(request):
    resultadosAm = []
    resultadosEu = []
    resultadosAo = []

    if request.method == 'POST':
        montoMin = request.POST['montoMin']
        montoMax = request.POST['montoMax']
        artista = request.POST['artista']
        continente = request.POST['continente']

        sql = """SELECT id_artista FROM artista WHERE nombre_artista = %s"""
        with connection.cursor() as cursor:
            cursor.execute(sql, artista)
            id = cursor.fetchone()[0]

        values = [
            (id,),
            (montoMin,),
            (montoMax,),
        ]

        if continente == 'America' or continente == '':
            sql = """SELECT r.id_contrato, tr.descripcion, r.monto
                FROM regalia_america r
                INNER JOIN tipo_regalia tr ON r.id_tipo_regalia = tr.id_tipo_regalia
                WHERE r.id_contrato IN (SELECT id_contrato FROM contrato_america WHERE id_artista = %s) 
                AND r.monto BETWEEN %s AND %s;"""
            with connection.cursor() as cursor:
                cursor.execute(sql, values)
                america = cursor.fetchall()

            for res in america:
                resultadosAm.append([res[0], res[1], f"{res[2]:.2f}", 'América'])
        
        if continente == 'Europa' or continente == '':
            sql = """SELECT r.id_contrato, tr.descripcion, r.monto
                FROM regalia_europa r
                INNER JOIN tipo_regalia tr ON r.id_tipo_regalia = tr.id_tipo_regalia
                WHERE r.id_contrato IN (SELECT id_contrato FROM contrato_europa WHERE id_artista = %s) 
                AND r.monto BETWEEN %s AND %s;"""
            with connection.cursor() as cursor:
                cursor.execute(sql, values)
                europa = cursor.fetchall()
            
            for res in europa:
                resultadosEu.append([res[0], res[1], f"{res[2]:.2f}", 'Europa'])

        if continente == 'Asia/Oceania' or continente == '':
            sql = """SELECT r.id_contrato, tr.descripcion, r.monto
                FROM regalia_asiaoceania r
                INNER JOIN tipo_regalia tr ON r.id_tipo_regalia = tr.id_tipo_regalia
                WHERE r.id_contrato IN (SELECT id_contrato FROM contrato_asiaoceania WHERE id_artista = %s) 
                AND r.monto BETWEEN %s AND %s;"""
            with connection.cursor() as cursor:
                cursor.execute(sql, values)
                asia = cursor.fetchall()

            for res in asia:
                resultadosAo.append([res[0], res[1], f"{res[2]:.2f}", 'Asia/Oceania'])

        
    sql = """SELECT nombre_artista FROM artista;"""
    with connection.cursor() as cursor:
        cursor.execute(sql)
        nombres = cursor.fetchall()
    opciones_nombres = [
        
    ]
    for nombre in nombres:
        option_value = nombre[0]  # Extract artist name from tuple
        option_text = (option_value, option_value)
        opciones_nombres.append(option_text)


    return render(request, 'paginas/regalias.html', {'nombres': opciones_nombres, 'america': resultadosAm, 'europa': resultadosEu, 'asia': resultadosAo})

def inspeccionAlbum(request):
    canciones_resultado = []
    if request.method == 'POST':
        album = request.POST['album']
        sql = """SELECT c.titulo, c.duracion, a.titulo AS titulo_album, a.fecha_lanzamiento, a.precio, a.edicion_especial
            FROM cancion c
            JOIN album a ON c.id_album = a.id_album
            WHERE a.titulo = %s
            ORDER BY c.titulo ASC;"""
        with connection.cursor() as cursor:
            cursor.execute(sql, album)
            canciones = cursor.fetchall()

        for can in canciones:
            canciones_resultado.append([can[0], can[1], can[2], can[3].strftime('%d-%m-%Y'), f"{can[4]:.2f}", 'Especial' if can[5] == 1 else 'Normal'])


    sql = """SELECT titulo FROM album;"""
    with connection.cursor() as cursor:
        cursor.execute(sql)
        albums = cursor.fetchall()
    opciones_albums = [
        
    ]
    for nombre in albums:
        option_value = nombre[0]  # Extract artist name from tuple
        option_text = (option_value, option_value)
        opciones_albums.append(option_text)


    return render(request, 'paginas/inspeccionAlbum.html', {'albums': opciones_albums, 'canciones': canciones_resultado})

def ventas(request):
    resultadosAm = []
    resultadosEu = []
    resultadosAo = []

    if request.method == 'POST':
        inicio = request.POST['fecha-inicio']
        final = request.POST['fecha-fin']
        album = request.POST['album']
        continente = request.POST['continente']

        values = [
            (inicio,),
            (final,),
            (album,),
        ]

        if continente == 'America' or continente == '':
            sql = """SELECT v.id_venta, v.fecha_venta, v.cantidad, t.descripcion AS tipo_venta, s.nombre AS nombre_sede 
                FROM venta_america v 
                JOIN tipo_venta t ON v.id_tipo_venta = t.id_tipo_venta 
                JOIN album a ON v.id_album = a.id_album 
                JOIN sede s ON v.id_sede = s.id_sede 
                WHERE v.fecha_venta BETWEEN %s AND %s 
                AND a.titulo = %s;"""
            with connection.cursor() as cursor:
                cursor.execute(sql, values)
                america = cursor.fetchall()

            for res in america:
                resultadosAm.append([res[0], res[1].strftime('%d-%m-%Y'), f"{res[2]:.2f}", res[3], res[4], 'América'])
        
        if continente == 'Europa' or continente == '':
            sql = """SELECT v.id_venta,
                    v.fecha_venta,
                    v.cantidad,
                    t.descripcion AS tipo_venta,
                    s.nombre AS nombre_sede
                FROM venta_europa v
                JOIN tipo_venta t ON v.id_tipo_venta = t.id_tipo_venta
                JOIN album a ON v.id_album = a.id_album
                JOIN sede s ON v.id_sede = s.id_sede
                WHERE v.fecha_venta BETWEEN %s AND %s
                AND a.titulo = %s;"""
            with connection.cursor() as cursor:
                cursor.execute(sql, values)
                europa = cursor.fetchall()

            for res in europa:
                resultadosEu.append([res[0], res[1].strftime('%d-%m-%Y'), f"{res[2]:.2f}", res[3], res[4], 'Europa'])

            if continente == 'Asia/Oceania' or continente == '':
                sql = """SELECT v.id_venta,
                        v.fecha_venta,
                        v.cantidad,
                        t.descripcion AS tipo_venta,
                        s.nombre AS nombre_sede
                    FROM venta_asiaoceania v
                    JOIN tipo_venta t ON v.id_tipo_venta = t.id_tipo_venta
                    JOIN album a ON v.id_album = a.id_album
                    JOIN sede s ON v.id_sede = s.id_sede
                    WHERE v.fecha_venta BETWEEN %s AND %s
                    AND a.titulo = %s;"""
                with connection.cursor() as cursor:
                    cursor.execute(sql, values)
                    asia = cursor.fetchall()

                for res in asia:
                    resultadosAo.append([res[0], res[1].strftime('%d-%m-%Y'), f"{res[2]:.2f}", res[3], res[4], 'Asia/Oceanía'])

    sql = """SELECT id_album, titulo FROM album;"""
    with connection.cursor() as cursor:
        cursor.execute(sql)
        albums = cursor.fetchall()
    opciones_albums = [
        
    ]
    for nombre in albums:
        option_text = (nombre[1], nombre[1])
        opciones_albums.append(option_text)

    return render(request, 'paginas/ventas.html', {'albums': opciones_albums, 'america': resultadosAm, 'europa': resultadosEu, 'asia': resultadosAo})