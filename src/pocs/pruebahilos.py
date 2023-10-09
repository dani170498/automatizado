import json
import re
from tqdm import tqdm
from colorama import init, Fore, Back, Style
import threading

# Función para buscar coincidencias en un subconjunto de elementos
def buscar_coincidencias_subconjunto(elemento_data, plugins_data, coincidencias):
    for elemento in elemento_data:
        nombre_elemento = elemento.get("nombre", "")
        version_elemento = elemento.get("version", "")
        url_elemento = elemento.get("url","")
        encontrada = False

        for plugin in plugins_data:
            nombre_plugin = plugin.get("nombre", "")
            version_plugin = plugin.get("version", "")

            if (re.fullmatch(nombre_elemento, nombre_plugin) and
                re.fullmatch(version_elemento, version_plugin)):

                elemento["cpename"] = plugin.get("cpename", "")
                coincidencia = {
                    "nombre": nombre_elemento,
                    "version": version_elemento,
                    "cpename": elemento["cpename"],
                    "url": url_elemento
                }
                coincidencias.append(coincidencia)

                print(Fore.CYAN+f"Coincidencia encontrada - Nombre: {nombre_elemento}, Versión: {version_elemento}, cpename: {elemento['cpename']} para: {url_elemento}"+Fore.RESET)

                encontrada = True
                break

        if not encontrada:
            print(Fore.MAGENTA+f"No se encontró coincidencia para - Nombre: {nombre_elemento}, Versión: {version_elemento}"+Fore.RESET)

# Cargar los datos de elemento.json y plugins.json
with open('/home/daniel/automatizado/diccionario/elemento.json', 'r') as f:
    elemento_data = json.load(f)

with open('/home/daniel/automatizado/diccionario/plugins.json', 'r') as f:
    plugins_data = json.load(f)

# Crear una lista para almacenar las coincidencias
coincidencias = []

# Número de hilos que deseas utilizar
num_threads = 10  # Puedes ajustar este valor según tus necesidades

# Dividir los elementos en subconjuntos para cada hilo
elemento_data_split = [elemento_data[i:i + len(elemento_data) // num_threads] for i in range(0, len(elemento_data), len(elemento_data) // num_threads)]

threads = []

# Inicializar la barra de progreso
with tqdm(total=len(elemento_data)) as pbar:
    # Crear hilos y ejecutar la búsqueda en paralelo
    for i in range(num_threads):
        thread = threading.Thread(target=buscar_coincidencias_subconjunto, args=(elemento_data_split[i], plugins_data, coincidencias))
        thread.start()
        threads.append(thread)

    # Esperar a que todos los hilos terminen
    for thread in threads:
        thread.join()
        pbar.update(len(elemento_data_split[i]))

# Guardar las coincidencias en un nuevo archivo JSON
with open('/home/daniel/automatizado/diccionario/coincidencias.json', 'w') as f:
    json.dump(coincidencias, f, indent=4)

print("Coincidencias encontradas y guardadas en coincidencias.json")
