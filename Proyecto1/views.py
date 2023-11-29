# Proyecto1/views.py
import os
import time
from django.http import HttpResponse
import datetime
from django.template import Template, Context
from django.template.loader import get_template
from urllib.parse import urlsplit, unquote

def inicioBuscador(request):
    docExterno = get_template('inicioBuscador.html')
    documento = docExterno.render()

    return HttpResponse(documento)

def buscador(request, buscar):
    tiempoInicio = time.time()
    (resultados, cont) = buscar_palabras(buscar)
    tiempoFin = time.time()
    tiempo = datetime.timedelta(seconds=(tiempoFin - tiempoInicio))
    
    docExterno = get_template('buscador.html')
    documento = docExterno.render({'buscar':buscar, 'links': resultados, 'cont': cont, 'tiempo': tiempo})

    return HttpResponse(documento)

def obtener_nombre_sitio_web(url):
    # Parsear la URL
    parsed_url = urlsplit(url)

    # Extraer el nombre de la página y decodificar la URL
    nombre_pagina = unquote(parsed_url.path.strip('/'))

    # Reemplazar los guiones bajos con espacios
    nombre_pagina = nombre_pagina.replace('_', ' ')

    # Eliminar el prefijo "wiki_"
    if nombre_pagina.startswith("wiki_") or nombre_pagina.startswith("wiki/"):
        nombre_pagina = nombre_pagina[len("wiki_"):]

    # Devolver el nombre de la página
    return nombre_pagina

def buscar_palabras(frase):
    # Obtén la ruta del archivo utilizando BASE_DIR
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, 'prueba.txt')

    with open(file_path, 'r', encoding='utf-8') as file:
        contenido = file.read()

    diccionario = eval(contenido)

    cont = 0
    resultados = []
    noDuplicados = set()

    # Convertir la frase en una lista de palabras
    palabras = frase.lower().split()

    for clave, valores in diccionario.items():
        if any(palabra.lower() == clave.lower() for palabra in palabras):
            for url, frecuencia in valores:
                if url not in noDuplicados:
                    nombre_sitio_web = obtener_nombre_sitio_web(url)
                    resultados.append((url, nombre_sitio_web, frecuencia))
                    noDuplicados.add(url)
                    cont+=1
                else:
                    # Buscar en resultados y actualizar la frecuencia
                    for i, (url_existente, _, frecuencia_existente) in enumerate(resultados):
                        if url_existente == url:
                            resultados[i] = (_, _, frecuencia_existente + frecuencia)
                            break

    resultados_ordenados = sorted(resultados, key=lambda x: x[2], reverse=True)
    # resultados_sin_frecuencia = [(url, nombre_sitio_web) for url, nombre_sitio_web, _ in resultados_ordenados]

    # print(f"Palabras buscadas: {palabras}")
    # print(f"Resultados sin frecuencia: {resultados_ordenados}")

    return resultados_ordenados, cont








































# class Persona(object):
#     def __init__(self, nombre, apellido):
#         self.nombre = nombre
#         self.apellido = apellido

# def saludo(request):
#     # nombre = "Juan"
#     p1 = Persona("Profesor Juan", "Díaz")
#     ahora = datetime.datetime.now()
#     temasDelCurso = ["Plantillas", "Modelos", "Formularios", "Vistas", "Despliegue"]

#     # docExterno = open("C:/Users/juanp/Documents/Archivos UATx/Materias/7mo Semestre/Recuperación de Información/3er Parcial/Proyecto1/Proyecto1/Plantillas/saludo.html")
#     # plt = Template(docExterno.read())
#     # docExterno.close()

#     docExterno = get_template('saludo.html')

#     # ctx = Context({"nombrePersona":p1.nombre, "apellidoPersona": p1.apellido, "momentoActual": ahora, "temas": temasDelCurso})
#     # documento = plt.render(ctx)
#     documento = docExterno.render({"nombrePersona":p1.nombre, "apellidoPersona": p1.apellido, "momentoActual": ahora, "temas": temasDelCurso})

#     return HttpResponse(documento)

# def despedida(request):
#     return HttpResponse("Adiós.")

# def dameFecha(request):
#     fechaActual = datetime.datetime.now()

#     documento = """
#     <html>
#     <body>
#     <h2>
#     Fecha y hora actuales: %s
#     </h2>
#     </body>
#     </html>""" % fechaActual

#     return HttpResponse(documento)

# def calculaEdad(request, edad, agno):
#     # edadActual = edad
#     periodo = agno - 2019
#     edadFutura = edad + periodo

#     documento = """
#     <html>
#     <body>
#     <h2>
#     En el año %s tendrás %s años
#     </h2>
#     </body>
#     </html>""" % (agno, edadFutura)
    
#     return HttpResponse(documento)
