import json

def procesar_json(entrada, salida):
    # Leer el archivo JSON de entrada
    with open(entrada, 'r', encoding='utf-8') as f:
        json_data = f.read()

    # Cargar el JSON
    data = json.loads(json_data)

    # Acceso a la lista de sitios en el JSON
    sitios = data.get('sitios', [])

    # Iteración a través de los sitios y modificación de los objetos JSON
    for sitio in sitios:
        url = sitio['url']
        subcadenas = url.split('/')
        plugin = subcadenas[-3]

        # Reemplazar barras "-" con barras bajas "_"
        #plugin = plugin.replace('-', '_')

        # Cambiar el atributo 'title' a 'nombre' y convertir a minúsculas
        sitio['nombre'] = sitio.pop('title').lower()

        # Agregar las claves 'plugin' y 'tag' al objeto JSON actual
        sitio['tipo'] = plugin
        sitio['cpename'] = ""

    # Guardar los datos actualizados en el archivo JSON de salida
    with open(salida, 'w', encoding='utf-8') as f:
        json.dump(sitios, f, indent=4, ensure_ascii=False)

    print("Datos actualizados y guardados en 'elemento.json'")

