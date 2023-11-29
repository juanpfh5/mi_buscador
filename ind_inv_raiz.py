import os
import re
import sys
import time
import aiohttp
import asyncio
import datetime
from typing import Counter
from bs4 import BeautifulSoup
from plyer import notification
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

COMMONWORDS = set(word.lower() for word in stopwords.words('english'))
stemmer = PorterStemmer()

diccionario = {}

def enviarNotificacion(titulo, mensaje):
    notification.notify(
        title=titulo,
        message=mensaje,
        timeout=10
    )

def imprimirTXT(diccionario, archivo_salida):
    with open(archivo_salida, "w", encoding="utf-8") as salidaFile:
        salidaFile.write("{\n")
        for palabra, lista_urls in diccionario.items():
            # Ordenar las URLs por frecuencia
            lista_urls_ordenadas = sorted(lista_urls, key=lambda x: x[1], reverse=True)

            salidaFile.write(f'\t"{palabra}" : [')
            for index, (url, cont) in enumerate(lista_urls_ordenadas):
                salidaFile.write(f'("{url}", {cont})')
                if index != len(lista_urls_ordenadas) - 1:
                    salidaFile.write(',')
            salidaFile.write("],\n")
        salidaFile.write("}")

def manejarBody(url, bodyEtiq):
    bodyEtiq = re.sub(r"[{}]+".format(re.escape("-—−–/_.&=?¡}]>)")), " ", bodyEtiq.translate(
        str.maketrans("", "", ",¿!\"#$%('|°\\;:{[^+*~<\t©✓—“”⸿¶⌑◊☞❧‡†⟩⟨«›‹‘®℗‖¦⁀⌀‱‰ªº№⸮⸗⹀‒⁂…‴″′’‐𞥞꩷႟߹🔛🆙！︕ꜟꜞꜝ⹓❣️❣❢❗❕⚠⁉️⁉⁈⸘‽‼️⇧⁄\¬×ˀᤃᤦᤄᤊᤇᤐᤤᤔᤚᤗᤖᤥᤂᤌ᥄ᤚᤦᤛᤅ᥄ᤂᤥᤆᤌᤙᤄᤨᤘᤑᤐᤚᤢ᥄﹗՜·⊙⊕○↑↑↻⇄↑∇δ□⌓⯹∞∓±⩱⩲ʃǂʼ")).lower().strip())

    bodyEtiq = [stemmer.stem(word) for word in bodyEtiq.split() if word not in COMMONWORDS]

    dic = Counter(bodyEtiq)

    for key, value in dic.items():
        if key in diccionario:
            diccionario[key].append((url, value))
        else:
            diccionario[key] = [(url, value)]

async def procesarURL(url, session):
    try:
        async with session.get(url) as response:
            if 200 <= response.status < 299:
                page = await response.text()
                soup = BeautifulSoup(page, 'html.parser')
                bodyEtiq = soup.find("body")

                if bodyEtiq:
                    classes_to_remove = [
                        re.compile(r'\bmw-jump-link\b'),
                        re.compile(r'\bvector-dropdown\b'),
                        re.compile(r'\bvector-pinned-container\b'),
                        re.compile(r'\bvector-header-container\b'),
                        re.compile(r'\bvector-page-toolbar\b'),
                        re.compile(r'\bvector-body-before-content\b'),
                        re.compile(r'\bprintfooter\b'),
                        re.compile(r'\bvector-settings\b'),
                        re.compile(r'\bmw-hidden-catlinks\b'),
                        re.compile(r'\bmw-footer-container\b'),
                    ]

                    for elem in bodyEtiq.find_all(True):
                        if any(elem.has_attr("class") and any(class_pattern.search(c) for c in elem["class"]) for class_pattern in classes_to_remove):
                            elem.extract()

                    bodyEtiq = " ".join(bodyEtiq.stripped_strings)

                    await manejarBody(url, bodyEtiq)
    except Exception as e:
        pass

async def obtenerURLS(archivo_entrada):
    try:
        with open(archivo_entrada, "r", encoding="utf-8") as entradaFile:
            for line in entradaFile:
                yield line.strip()
    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo {archivo_entrada}")
        sys.exit(1)

def eliminarArchivo(archivo):
    if os.path.exists(archivo):
        os.remove(archivo)

def limpiarConsola():
    os.system('cls' if os.name == 'nt' else 'clear')

async def main(archivo_entrada, archivo_salida):
    nombreArchivo = os.path.basename(__file__)
    limpiarConsola()

    print(f" = = = = = = = Programa: {nombreArchivo} = = = = = = = \n")

    tiempoInicio = time.time()

    urls = {url async for url in obtenerURLS(archivo_entrada)}

    async with aiohttp.ClientSession() as session:
        tasks = [procesarURL(url, session) for url in urls]
        await asyncio.gather(*tasks)

    eliminarArchivo(archivo_salida)
    imprimirTXT(diccionario, archivo_salida)

    tiempoFin = time.time()

    print(f"Archivo '{archivo_salida}' generado exitosamente.")
    tiempo = datetime.timedelta(seconds=(tiempoFin - tiempoInicio))
    print(f"Tiempo de ejecución: {tiempo}")

    enviarNotificacion("Ejecución finalizada 👨‍💻✨", f"El programa {nombreArchivo} ha finalizado su ejecución en {tiempo}.\n\n")

if __name__ == "__main__":
    ARCHIVO_ENTRADA = "urls.txt"
    ARCHIVO_SALIDA = "raiz_ind_inv.txt"
    asyncio.run(main(ARCHIVO_ENTRADA, ARCHIVO_SALIDA))