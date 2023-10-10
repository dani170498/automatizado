import json
import os
import datetime
from src.descargarxml import descargar_descomprimir_filtrar
from src.procesarjson import procesar_json
from src.cdiccionario import CpeParser
from src.coincidencias import BuscadorCoincidencias
#from src.evaluacion import main as evaluacion_main
from src.evaluacion import VulnerabilityScanner
#from src.resultados import cargar_resultados_desde_archivo
from src.resultados import GeneradorPDF
#from src.eliminar_archivos import eliminar_archivo

def main():
    # Ejecuta la función descargar_descomprimir_filtrar para obtener el archivo de entrada
    descargar_descomprimir_filtrar()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    #procesarjson
    # Rutas de entrada y salida JSON
    entrada_json = "../diccionario/wordpress_plugin_theme.json"
    salida_json = "../diccionario/elemento.json"
    procesar_json(entrada_json, salida_json)
    #print("todo terminado, guardado en la ruta correspondiente")
    #creardiccionario
    # Ruta del archivo de entrada para parsear
    archivo_entrada= os.path.join(script_dir, "archivos/cpe.txt")
    ruta_salida = os.path.join(script_dir, "diccionario/plugins.json")
    parser = CpeParser(archivo_entrada)
    plugins = parser.parsear_cpe()
    with open(ruta_salida, "w") as archivo_salida:
        json.dump(plugins, archivo_salida, indent=4)

    print(f'SE CREO EL DICCIONARIO EN: {ruta_salida}')
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
    #evaluacion_main()
    api_key = "5659d884-5496-4211-9d15-79135985b3a1"
    json_path = 'diccionario/coincidencias.json'
    output_path = 'resultados.json'
    scanner = VulnerabilityScanner(api_key)
    scanner.procesar_sitios(json_path, output_path)
    
    #generar pdf

    ruta_archivo_json = "resultados.json"
    nombre_archivo_pdf = f"reportes/resultados_escaneo_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.pdf"
    generador_pdf = GeneradorPDF(ruta_archivo_json)
    generador_pdf.generar_pdf(nombre_archivo_pdf)
    

    #eliminar archivos
#    rutas_a_eliminar = [
#        '/home/daniel/automatizado/diccionario/diccionario.json',
#        '/home/daniel/automatizado/diccionario/elemento.json',
#        '/home/daniel/automatizado/diccionario/evaluar.json',
#        '/home/daniel/automatizado/archivos/cpe.txt',
#        '/home/daniel/automatizado/resultados.json'
#    ]
#    for ruta in rutas_a_eliminar:
#        eliminar_archivo(ruta)

if __name__ == "__main__":
    main()

