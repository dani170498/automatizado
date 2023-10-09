import json
import re
import os
from tqdm import tqdm
from colorama import init, Fore, Back, Style

class BuscadorCoincidencias:
    def __init__(self, elemento_path, plugins_path, coincidencias_path):
        self.elemento_path = elemento_path
        self.plugins_path = plugins_path
        self.coincidencias_path = coincidencias_path

    def cargar_json(self, ruta):
        with open(ruta, 'r') as archivo:
            return json.load(archivo)

    def guardar_json(self, datos, ruta):
        with open(ruta, 'w') as archivo:
            json.dump(datos, archivo, indent=4)

    def buscar_coincidencias(self):
        # Cargar los datos de elemento.json y plugins.json
        with open(self.elemento_path, 'r') as f:
            elemento_data = json.load(f)

        with open(self.plugins_path, 'r') as f:
            plugins_data = json.load(f)

        # Crear una lista para almacenar las coincidencias
        coincidencias = []

        # Inicializar la barra de progreso
        with tqdm(total=len(elemento_data)) as pbar:
            # Iterar a través de los elementos en elemento.json
            for elemento in elemento_data:
                nombre_elemento = elemento.get("nombre", "")
                version_elemento = elemento.get("version", "")
                url_elemento = elemento.get("url","")
                # Variable para controlar si se encontró una coincidencia
                encontrada = False

                # Iterar a través de los elementos en plugins.json
                for plugin in plugins_data:
                    nombre_plugin = plugin.get("nombre", "")
                    version_plugin = plugin.get("version", "")

                    # Utilizar expresiones regulares para verificar la coincidencia exacta
                    if (re.fullmatch(nombre_elemento, nombre_plugin) and
                        re.fullmatch(version_elemento, version_plugin)):

                        # Copiar el valor de cpename de plugins.json a elemento.json
                        elemento["cpename"] = plugin.get("cpename", "")

                        # Agregar la coincidencia a la lista
                        coincidencia = {
                            "nombre": nombre_elemento,
                            "version": version_elemento,
                            "cpename": elemento["cpename"],
                            "url":url_elemento
                        }
                        coincidencias.append(coincidencia)

                        # Imprimir cpename, nombre y versión de la coincidencia
                        print(Fore.CYAN+f"Coincidencia encontrada - Nombre: {nombre_elemento}, Versión: {version_elemento}, cpename: {elemento['cpename']}"+Fore.RESET)

                        encontrada = True
                        break  # Salir del bucle cuando se encuentra una coincidencia

                if not encontrada:
                    print(Fore.MAGENTA+f"No se encontró coincidencia para - Nombre: {nombre_elemento}, Versión: {version_elemento}"+Fore.RESET)

                pbar.update(1)  # Actualizar la barra de progreso

        # Guardar las coincidencias en un nuevo archivo JSON
        with open(self.coincidencias_path, 'w') as f:
            json.dump(coincidencias, f, indent=4)

        print("Coincidencias encontradas y guardadas en coincidencias.json")

def main():
    elemento_path = 'diccionario/elemento.json'
    plugins_path = 'diccionario/plugins.json'
    coincidencias_path = 'diccionario/coincidencias.json'

    elemento_path = os.path.abspath(elemento_path)
    plugins_path = os.path.abspath(plugins_path)
    coincidencias_path = os.path.abspath(coincidencias_path)

    buscador = BuscadorCoincidencias(elemento_path, plugins_path, coincidencias_path)
    buscador.buscar_coincidencias()

if __name__ == "__main__":
    init(autoreset=True)  # Inicializar colorama para el reseteo automático de colores
    main()

