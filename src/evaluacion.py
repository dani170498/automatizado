import json
import requests
import time
from tqdm import tqdm

COLOR_BLUE = "\x1b[34m"
COLOR_RED = "\x1b[31m"
COLOR_RESET = "\x1b[0m"

def procesar_sitios(json_path, output_path):
    api_key = "5659d884-5496-4211-9d15-79135985b3a1"
    nist_base_url = "https://services.nvd.nist.gov/rest/json/cves/2.0?cpeName="
    requests_counter = 0
    output_data = []

    with open(json_path, 'r') as json_file:
        data = json.load(json_file)

    # Usa tqdm para crear una barra de progreso
    for sitio in tqdm(data, desc="Procesando Sitios"):
        tag_json = sitio["cpename"]
        version_json = sitio["version"]
        url_json = sitio['url']
        plugin_json = sitio['nombre']

        # Validar si cpename está vacío
        if not tag_json:
            print('****************INICIANDO ESCANEO*****************************************/////')
            print('************************************************************************************')
            print(COLOR_RED + f"cpename está vacío para '{plugin_json}' y versión '{version_json}' en '{url_json}'. Saltando solicitud." + COLOR_RESET)
            print('************************************************************************************')
            continue

        nist_url = nist_base_url + tag_json

        headers = {
            "api_key": api_key
        }

        try:
            # Enviar solicitud a la API de NIST
            response = requests.get(nist_url, headers=headers)
            response.raise_for_status()  # Lanza una excepción si la solicitud no es exitosa

            nist_data = response.json()
            # Verificar si se encontraron vulnerabilidades
            vulnerabilities = nist_data.get("vulnerabilities", [])

            if vulnerabilities:
                found = True  # Se encontró una coincidencia
                for vulnerability in vulnerabilities:
                    # Extraer el CVE ID
                    cve_id = vulnerability.get("cve", {}).get("id", "")
                    # Extraer la descripción CVE
                    cve_description = vulnerability.get("cve", {}).get("descriptions", [{}])[0].get("value", "")

                    # Extraer la lista de métricas
                    metrics_list = vulnerability.get("cve", {}).get("metrics", [{}])

                    # Crear un diccionario con la información deseada
                    result = {
                        "Match": url_json,
                        "Plugin": plugin_json,
                        "Version": version_json,
                        "CVE ID": cve_id,
                        "CVE Descripcion": cve_description,
                        "Metrics": metrics_list,  # Inicializamos una lista vacía para Metrics
                        "prueba": nist_url
                    }

                    output_data.append(result)
                    print('******************************************************************************************')
                    print(COLOR_BLUE + f"Coincidencia encontrada para '{plugin_json}'"+ COLOR_RESET)
                    print(COLOR_BLUE+f"version '{version_json}'")
                    print(f"en URL: '{url_json}'"+ COLOR_RESET)
                    print('******************************************************************************************')
                    print(json.dumps(result, indent=2))
            else:
                print('*******************************************************************')
                print(COLOR_RED + f"No se encontraron coincidencias para '{plugin_json}'")
                print(f"version : '{version_json}'")
                print(f"en : '{url_json}'"+COLOR_RESET)
                print('*******************************************************************')

        except requests.exceptions.HTTPError as e:
            print('*************************************************************************************')
            print(COLOR_RED+f"Error al obtener datos de NIST para '{plugin_json}' y versión '{version_json}' en '{url_json}': {e}"+COLOR_RESET)
            print('*************************************************************************************')

        # pausa 60 segundos
        requests_counter += 1
        if requests_counter % 5 == 0:
            print("Tomando un descanso de 60 segundos...")
            time.sleep(60)

    # salida en un archivo JSON
    with open(output_path, 'w') as output_file:
        json.dump(output_data, output_file, indent=2)

    # Imprimir la salida en formato JSON al final
    print("Resultados almacenados en:", output_path)

def main():
    json_path = '/home/daniel/automatizado/diccionario/evaluar.json'
    output_path = '/home/daniel/automatizado/resultados.json'
    procesar_sitios(json_path, output_path)

if __name__ == "__main__":
    main()
