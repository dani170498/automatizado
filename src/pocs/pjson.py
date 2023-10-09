import json
import os

def procesar_json(entrada, salida):
    # Obtener la ubicación actual del script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Construir las rutas completas para la entrada y salida JSON
    entrada_json = os.path.join(script_dir, entrada)
    salida_json = os.path.join(script_dir, salida)

    # Leer el archivo JSON de entrada
    with open(entrada_json, 'r', encoding='utf-8') as f:
        json_data = f.read()

    # Cargar el JSON
    data = json.loads(json_data)

    # Acceso a la lista de sitios en el JSON
    sitios = data.get('sitios', [])

    # Lista para almacenar los objetos JSON resultantes
    objetos_json = []

    # Iteración a través de los sitios y creación de objetos JSON
    for sitio in sitios:
        url = sitio['url']
        subcadenas = url.split('/')
        plugin = subcadenas[-3]

        # Cambiar el atributo 'title' a 'nombre' y convertir a minúsculas
        sitio['nombre'] = sitio.pop('name').lower()

        # Reemplazar guiones con espacios en el nombre
        sitio['nombre'] = sitio['nombre'].replace('-', ' ')

        # Agregar las claves 'plugin' y 'tag' al objeto JSON actual
        sitio['tipo'] = plugin
        sitio['cpename'] = ""

        # Reorganizar el orden de las claves en el objeto JSON
        objeto_ordenado = {
            'nombre': sitio['nombre'],
            'version': sitio.get('version', ""),
            'cpename': sitio.get('cpename', ""),
            'url': sitio['url'],
            'themes': sitio.get('themes', "")
        }

        # Agregar el objeto JSON actual a la lista
        objetos_json.append(objeto_ordenado)

    # Eliminar el campo 'sitios' del JSON resultante
    data.pop('sitios')

    # Guardar los datos actualizados en el archivo JSON de salida
    with open(salida_json, 'w', encoding='utf-8') as f:
        json.dump(objetos_json, f, indent=4, ensure_ascii=False)

    print(f"Datos actualizados y guardados en '{salida}'")

# Ejemplo de uso
if __name__ == "__main__":
    entrada = "../diccionario/wordpress_plugin_theme.json"  # Ruta relativa de entrada
    salida = "../diccionario/elemento.json"  # Ruta relativa de salida
    procesar_json(entrada, salida)

