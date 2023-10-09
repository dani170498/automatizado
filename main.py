import json
import os
from src.descargarxml import descargar_descomprimir_filtrar
from src.procesarjson import procesar_json
from src.creardiccionario import CpeParser
from src.coincidencias import BuscadorCoincidencias
from src.evaluacion import main as evaluacion_main
from src.resultados import cargar_resultados_desde_archivo
from src.eliminar_archivos import eliminar_archivo


def main():
    # Ejecuta la función descargar_descomprimir_filtrar para obtener el archivo de entrada
    descargar_descomprimir_filtrar()
    script_dir = os.path.dirname(os.path.abspath(__file__))


    #procesarjson
    # Rutas de entrada y salida JSON
    entrada_json = "../diccionario/wordpress_plugin_theme.json"
    salida_json = "../diccionario/elemento.json"
    procesar_json(entrada_json, salida_json)
    #print("todo terminado, guardado en la ruta correspondienter")

    #creardiccionario
    # Ruta del archivo de entrada para parsear
    archivo_entrada="/archivos/cpe.txt"
    archivo_salida = "/diccionario/plugins.json"
    parser = CpeParser(archivo_entrada)
    parser.main = (archivo_salida)
    print(f'todo terminado, guardado en la ruta correspondiente: "{archivo_salida}"')

    # buscar coincidencias entre diccionario y plugins extraidos

    elemento_path = 'diccionario/elemento.json'
    plugins_path = 'diccionario/plugins.json'
    coincidencias_path = 'diccionario/coincidencias.json'
    elemento_path = os.path.abspath(elemento_path)
    plugins_path = os.path.abspath(plugins_path)
    coincidencias_path = os.path.abspath(coincidencias_path)
    buscador = BuscadorCoincidencias(elemento_path, plugins_path, coincidencias_path)
    buscador.buscar_coincidencias()


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

