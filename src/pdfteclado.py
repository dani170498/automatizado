import json
from reportlab.lib.pagesizes import landscape, letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, PageBreak, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

# Función para buscar coincidencias en el JSON de un archivo
def buscar_coincidencias_en_archivo(ruta_archivo, dato_busqueda):
    try:
        with open(ruta_archivo, 'r') as archivo:
            data = json.load(archivo)
            coincidencias = []

            for item in data:
                if "Match" in item and dato_busqueda in item["Match"]:
                    coincidencias.append(item)

            return coincidencias
    
    except FileNotFoundError:
        return "El archivo no fue encontrado"
    except json.JSONDecodeError:
        return "Error al analizar el JSON del archivo"

# Ruta del archivo JSON
ruta_archivo_json = "/home/kali/apinist/resultados.json"

# Dato de entrada para buscar
dato_entrada = input("Ingrese el dominio a buscar: ")

# Llamamos a la función y obtenemos los resultados
resultado = buscar_coincidencias_en_archivo(ruta_archivo_json, dato_entrada)

# Nombre del archivo PDF de salida
nombre_archivo_pdf = f"/home/kali/apinist/resultados/resultados{dato_entrada}.pdf"

# Verificar si se encontraron coincidencias
if not resultado:
    print(f"No se encontraron coincidencias con '{dato_entrada}'.")
else:
    # Crear un documento PDF con orientación horizontal (paisaje)
    doc = SimpleDocTemplate(nombre_archivo_pdf, pagesize=landscape(letter), leftMargin=20, rightMargin=20)

    # Lista para almacenar los elementos del PDF
    elements = []

    styles = getSampleStyleSheet()
    style_normal = styles['Normal']

    # Crear una tabla para mostrar cada resultado en una página separada
    for item in resultado:
        # Extraer la sección 'cvssMetricV31' si existe
        cvss_metric = item.get("Metrics", {}).get("cvssMetricV31", [])
        if cvss_metric:
            base_severity = cvss_metric[0].get("cvssData", {}).get("baseSeverity", "")
        else:
            base_severity = ""

        # Crear una tabla de dos columnas para los datos de cabecera y los valores
        data = [["Dato", "Valor"]]
        data.extend([
            ["Match", item.get("Match", "")],
            ["Plugin", item.get("Plugin", "")],
            ["Version", item.get("Version", "")],
            ["CVE ID", item.get("CVE ID", "")],
            ["CVE Descripcion", Paragraph(item.get("CVE Descripcion", ""), style_normal)],
            ["Base Severity", base_severity],  # Agregar el valor de Base Severity
        ])

        # Definir el estilo de la tabla
        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ])  # Alineación superior (justificada)

        # Crear la tabla y aplicar el estilo
        tabla = Table(data, colWidths=[150, None])
        tabla.setStyle(table_style)

        # Agregar la tabla al documento
        elements.append(tabla)
        elements.append(PageBreak())  # Salto de página después de cada tabla

    # Construir el PDF
    doc.build(elements)

    print(f"Los resultados se han guardado en {nombre_archivo_pdf}")

