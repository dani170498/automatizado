import re
import json
import os

class CpeParser:
    def __init__(self, archivo_entrada):
        self.archivo_entrada = archivo_entrada

    def reemplazar_barras_bajas(self, cadena):
        # Reemplazar barras bajas con espacios
        return cadena.replace('_', ' ')

    def limpiar_nombre(self, nombre):
        # Remover caracteres no deseados y espacios extras
        nombre_limpio = re.sub(r'[^A-Za-z0-9\s]', '', nombre)
        return ' '.join(nombre_limpio.split())  # Eliminar espacios extras

    def parsear_cpe(self):
        plugins = []

        with open(self.archivo_entrada, 'r') as archivo:
            lineas_cpe = archivo.readlines()

            for linea in lineas_cpe:
                # Utilizamos una expresión regular para extraer los campos específicos
                match = re.match(r"cpe:2\.3:[a-z]:([^:]+):([^:]+):([^:]+):.*:wordpress:.*", linea)
                if match:
                    proveedor = match.group(1)
                    nombre = match.group(2)
                    version = match.group(3)
                    cpename = linea.strip()

                    # Reemplazar barras bajas y limpiar el nombre
                    nombre = self.reemplazar_barras_bajas(nombre)
                    nombre = self.limpiar_nombre(nombre)

                    plugin_info = {
                        "nombre": nombre,
                        "version": version,
                        "proveedor": proveedor,
                        "cpename": cpename
                    }

                    plugins.append(plugin_info)

        return plugins

if __name__ == "__main__":
    archivo_entrada = "../archivos/cpe.txt"

    parser = CpeParser(archivo_entrada)
    plugins = parser.parsear_cpe()

    # Definir la ruta de salida relativa a la carpeta 'diccionario'
    ruta_salida = "../diccionario/plugins.json"

    # Obtener la ruta absoluta
    ruta_absoluta = os.path.abspath(ruta_salida)

    # Guardar la información en un archivo JSON en la ruta absoluta
    with open(ruta_absoluta, "w") as archivo_salida:
        json.dump(plugins, archivo_salida, indent=4)
