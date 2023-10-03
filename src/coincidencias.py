import json
from tqdm import tqdm  # Importamos tqdm para la barra de progreso

def cargar_json(ruta):
    with open(ruta, 'r') as archivo:
        return json.load(archivo)

def guardar_json(datos, ruta):
    with open(ruta, 'w') as archivo:
        json.dump(datos, archivo, indent=4)

def buscar_coincidencias(diccionario, elementos):
    with tqdm(total=len(elementos)) as pbar:  # Inicializamos la barra de progreso
        for elemento in elementos:
            nombre_elemento2 = elemento.get("nombre", "")
            version_elemento2 = elemento.get("version", "")

            for entry in diccionario:
                nombre_elemento1 = entry.get("nombre", "")
                version_elemento1 = entry.get("version", "")

                if nombre_elemento1 in nombre_elemento2 and version_elemento1 == version_elemento2:
                    elemento["cpename"] = entry.get("cpename", "")
            pbar.update(1)  # Actualizamos la barra de progreso

def main():
    diccionario = cargar_json('/home/daniel/automatizado/diccionario/diccionario.json')
    elementos = cargar_json('/home/daniel/automatizado/diccionario/elemento.json')

    buscar_coincidencias(diccionario, elementos)

    guardar_json(elementos, '/home/daniel/automatizado/diccionario/evaluar.json')

if __name__ == "__main__":
    main()

