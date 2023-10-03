from src.descargarxml import descargar_descomprimir_filtrar
from src.procesarjson import procesar_json
from src.creardiccionario import CpeParser
import json
def main():
    # Ejecuta la función descargar_descomprimir_filtrar para obtener el archivo de entrada
    descargar_descomprimir_filtrar()

    # Rutas de entrada y salida JSON
    entrada_json = '/home/kali/automatizado/diccionario/lista.json'
    salida_json = '/home/kali/automatizado/diccionario/elemento.json'

    # Ruta del archivo de entrada para parsear
    archivo_entrada_cpe = "/home/kali/automatizado/archivos/cpe.txt"

    # Instancia la clase CpeParser y ejecuta el proceso de parseo
    parser = CpeParser(archivo_entrada_cpe)
    plugins = parser.parsear_cpe()

    # Guarda la información en un archivo JSON
    with open("/home/daniel/automatizado/diccionario/diccionario.json", "w") as archivo_salida_cpe:
        json.dump(plugins, archivo_salida_cpe, indent=4)

    # Luego puedes continuar con el procesamiento en procesar_json si es necesario.
    # procesar_json(entrada_json, salida_json)

if __name__ == "__main__":
    main()

