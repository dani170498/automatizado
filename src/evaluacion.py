import json
import requests
import time
from tqdm import tqdm
import os

class VulnerabilityScanner:
    COLOR_BLUE = "\x1b[34m"
    COLOR_RED = "\x1b[31m"
    COLOR_RESET = "\x1b[0m"

    def __init__(self, api_key):
        self.api_key = api_key
        self.nist_base_url = "https://services.nvd.nist.gov/rest/json/cves/2.0?cpeName="

    def procesar_sitios(self, json_path, output_path):
        requests_counter = 0
        output_data = []

        with open(json_path, 'r') as json_file:
            data = json.load(json_file)

        for sitio in tqdm(data, desc="Procesando Sitios"):
            tag_json = sitio["cpename"]
            version_json = sitio["version"]
            url_json = sitio['url']
            plugin_json = sitio['nombre']

            if not tag_json:
                print('****************INICIANDO ESCANEO*****************************************/////')
                print('************************************************************************************')
                print(self.COLOR_RED + f"cpename está vacío para '{plugin_json}' y versión '{version_json}' en '{url_json}'. Saltando solicitud." + self.COLOR_RESET)
                print('************************************************************************************')
                continue

            nist_url = self.nist_base_url + tag_json

            headers = {
                "api_key": self.api_key
            }

            try:
                response = requests.get(nist_url, headers=headers)
                response.raise_for_status()

                nist_data = response.json()
                vulnerabilities = nist_data.get("vulnerabilities", [])

                if vulnerabilities:
                    found = True
                    for vulnerability in vulnerabilities:
                        cve_id = vulnerability.get("cve", {}).get("id", "")
                        cve_description = vulnerability.get("cve", {}).get("descriptions", [{}])[0].get("value", "")
                        metrics_list = vulnerability.get("cve", {}).get("metrics", [{}])

                        result = {
                            "Match": url_json,
                            "Plugin": plugin_json,
                            "Version": version_json,
                            "CVE ID": cve_id,
                            "CVE Descripcion": cve_description,
                            "Metrics": metrics_list,
                            "prueba": nist_url
                        }

                        output_data.append(result)
                        print('******************************************************************************************')
                        print(self.COLOR_BLUE + f"Coincidencia encontrada para '{plugin_json}'" + self.COLOR_RESET)
                        print(self.COLOR_BLUE + f"version '{version_json}'")
                        print(f"en URL: '{url_json}'" + self.COLOR_RESET)
                        print('******************************************************************************************')
                        print(json.dumps(result, indent=2))
                else:
                    print('*******************************************************************')
                    print(self.COLOR_RED + f"No se encontraron coincidencias para '{plugin_json}'")
                    print(f"version : '{version_json}'")
                    print(f"en : '{url_json}'" + self.COLOR_RESET)
                    print('*******************************************************************')

            except requests.exceptions.HTTPError as e:
                print('*************************************************************************************')
                print(self.COLOR_RED + f"Error al obtener datos de NIST para '{plugin_json}' y versión '{version_json}' en '{url_json}': {e}" + self.COLOR_RESET)
                print('*************************************************************************************')

            requests_counter += 1
            if requests_counter % 4 == 0:
                print("Tomando un descanso de 60 segundos...")
                time.sleep(60)

        with open(output_path, 'w') as output_file:
            json.dump(output_data, output_file, indent=2)

        print("Resultados almacenados en:", output_path)

def main():
    api_key = "5659d884-5496-4211-9d15-79135985b3a1"
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Directorio del script actual
    json_path = os.path.join(script_dir, 'diccionario', 'coincidencias.json')  # Ruta relativa del archivo de entrada
    output_path = 'resultados.json'  # Ruta relativa del archivo de salida (en el directorio del script)
    scanner = VulnerabilityScanner(api_key)
    scanner.procesar_sitios(json_path, output_path)

if __name__ == "__main__":
    main()

