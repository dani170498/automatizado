import json

def procesar_json(entrada, salida):
    # Leer el archivo JSON de entrada
    with open(entrada, 'r') as f:
        json_data = f.read()

    # Cargar el JSON
    data = json.loads(json_data)

    # Acceso a una cadena de texto en el JSON
    sitios = data['sitios']

    # Iteración a través de los sitios y modificación de los objetos JSON
    for sitio in sitios:
        url = sitio['url']
        subcadenas = url.split('/')
        plugin = subcadenas[-3]

        # Reemplazar barras "-" con barras bajas "_"
        #plugin = plugin.replace('-', '_')

        # Agregar las claves 'plugin' y 'tag' al objeto JSON actual
        sitio['tipo'] = plugin
        sitio['cpename'] = ""

    # Guardar los datos actualizados en el archivo JSON de salida
    with open(salida, 'w') as f:
        json.dump(data, f, indent=4)

    print("Datos actualizados y guardados en 'elemento.json'")
