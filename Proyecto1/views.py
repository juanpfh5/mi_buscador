# Proyecto1/views.py

import os
import time
from django.http import HttpResponse
import datetime
from django.template import Template, Context
from django.template.loader import get_template
from urllib.parse import urlsplit, unquote
from nltk.stem import PorterStemmer

# Define la función buscar_palabras
def buscar_palabras(frase, diccionario, stemmer, no_duplicados):
    # Convertir la frase en un conjunto de palabras en minúsculas y con stemming
    palabras = set(stemmer.stem(palabra.lower()) for palabra in frase.split())
    resultados = []

    for clave, valores in diccionario.items():
        if any(stemmer.stem(palabra.lower()) == stemmer.stem(clave.lower()) for palabra in palabras):
            for url, frecuencia in valores:
                if url not in no_duplicados:
                    nombre_sitio_web = obtener_nombre_sitio_web(url)
                    resultados.append((url, nombre_sitio_web, frecuencia))
                    no_duplicados.add(url)

    resultados_ordenados = sorted(resultados, key=lambda x: x[2], reverse=True)
    cont = len(resultados_ordenados)

    return resultados_ordenados, cont

def inicioBuscador(request):
    docExterno = get_template('inicioBuscador.html')
    documento = docExterno.render()

    return HttpResponse(documento)

def buscador(request, buscar):
    tiempoInicio = time.time()
    resultados, cont = buscar_palabras(buscar, diccionario, stemmer, no_duplicados)
    tiempoFin = time.time()
    tiempo = datetime.timedelta(seconds=(tiempoFin - tiempoInicio))
    
    docExterno = get_template('buscador.html')
    documento = docExterno.render({'buscar':buscar, 'links': resultados, 'cont': cont, 'tiempo': tiempo})

    return HttpResponse(documento)

def obtener_nombre_sitio_web(url):
    parsed_url = urlsplit(url)
    nombre_pagina = unquote(parsed_url.path.strip('/'))

    nombre_pagina = nombre_pagina.replace('_', ' ')

    if nombre_pagina.startswith("wiki_") or nombre_pagina.startswith("wiki/"):
        nombre_pagina = nombre_pagina[len("wiki_"):]

    return nombre_pagina

# Obtén la ruta del archivo utilizando BASE_DIR
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_path = os.path.join(base_dir, 'raiz_ind_inv.txt')

# Lee el archivo una vez
with open(file_path, 'r', encoding='utf-8') as file:
    diccionario = eval(file.read())

# Inicializa el stemmer de NLTK
stemmer = PorterStemmer()

# Inicializa el conjunto de no_duplicados
no_duplicados = set()

# Ahora puedes llamar a la función con los argumentos precalculados
resultados, cont = buscar_palabras("tu_frase_aqui", diccionario, stemmer, no_duplicados)












































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
