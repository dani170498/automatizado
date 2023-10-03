import json
from src.descargarxml import descargar_descomprimir_filtrar
from src.procesarjson import procesar_json
from src.creardiccionario import CpeParser
from src.coincidencias import main as coincidencias_main
from src.evaluacion import main as evaluacion_main
from src.resultados import cargar_resultados_desde_archivo
from src.eliminar_archivos import eliminar_archivo


def main():
    # Ejecuta la función descargar_descomprimir_filtrar para obtener el archivo de entrada
    descargar_descomprimir_filtrar()

    #procesarjson
    # Rutas de entrada y salida JSON
    entrada_json = '/home/daniel/automatizado/diccionario/lista.json'
    salida_json = '/home/daniel/automatizado/diccionario/elemento.json'
    procesar_json(entrada_json, salida_json)

    #creardiccionario
    # Ruta del archivo de entrada para parsear
    archivo_entrada_cpe = "/home/daniel/automatizado/archivos/cpe.txt"

    # Instancia la clase CpeParser y ejecuta el proceso de parseo
    parser = CpeParser(archivo_entrada_cpe)
    plugins = parser.parsear_cpe()

    # Guarda la información en un archivo JSON
    with open("/home/daniel/automatizado/diccionario/diccionario.json", "w") as archivo_salida_cpe:
        json.dump(plugins, archivo_salida_cpe, indent=4)

    # Llama a la función main de coincidencias.py
    coincidencias_main()
    #evaluacion con la api de NIST
    evaluacion_main()
    #generar pdf
    ruta_archivo = '/home/daniel/automatizado/resultados.json'
    cargar_resultados_desde_archivo(ruta_archivo)
    #eliminar archivos
    rutas_a_eliminar = [
        '/home/daniel/automatizado/diccionario/diccionario.json',
        '/home/daniel/automatizado/diccionario/elemento.json',
        '/home/daniel/automatizado/diccionario/evaluar.json',
        '/home/daniel/automatizado/archivos/cpe.txt',
        '/home/daniel/automatizado/resultados.json'
    ]

    for ruta in rutas_a_eliminar:
        eliminar_archivo(ruta)

if __name__ == "__main__":
    main()

