import json
import re
from tqdm import tqdm
from colorama import init, Fore, Back, Style


# Cargar los datos de elemento.json y plugins.json
with open('/home/daniel/automatizado/diccionario/elemento.json', 'r') as f:
    elemento_data = json.load(f)

with open('/home/daniel/automatizado/diccionario/plugins.json', 'r') as f:
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
                print(Fore.CYAN+f"Coincidencia encontrada - Nombre: {nombre_elemento}, Versión: {version_elemento}, cpename: {elemento['cpename']} para: {url_elemento}"+Fore.RESET)

                encontrada = True
                break  # Salir del bucle cuando se encuentra una coincidencia

        if not encontrada:
            print(Fore.MAGENTA+f"No se encontró coincidencia para - Nombre: {nombre_elemento}, Versión: {version_elemento}"+Fore.RESET)

        pbar.update(1)  # Actualizar la barra de progreso

# Guardar las coincidencias en un nuevo archivo JSON
with open('/home/daniel/automatizado/diccionario/coincidencias.json', 'w') as f:
    json.dump(coincidencias, f, indent=4)

print("Coincidencias encontradas y guardadas en coincidencias.json")

