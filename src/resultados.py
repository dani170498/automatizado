import json
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, PageBreak, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.platypus.flowables import KeepInFrame

# Función para cargar todos los resultados del JSON
def cargar_resultados_desde_archivo(ruta_archivo):
    try:
        with open(ruta_archivo, 'r') as archivo:
            data = json.load(archivo)
            return data
    except FileNotFoundError:
        return "El archivo no fue encontrado"
    except json.JSONDecodeError:
        return "Error al analizar el JSON del archivo"

# Ruta del archivo JSON
ruta_archivo_json = "/home/kali/apinist/resultados.json"

# Cargar todos los resultados desde el archivo JSON
resultados = cargar_resultados_desde_archivo(ruta_archivo_json)

# Nombre del archivo PDF de salida
nombre_archivo_pdf = "/home/kali/apinist/resultados/resultados_escaneo.pdf"

# Crear un documento PDF con tamaño de hoja en carta (8.5 x 11 pulgadas) y orientación horizontal
doc = SimpleDocTemplate(nombre_archivo_pdf, pagesize=landscape(letter), leftMargin=20, rightMargin=20)

# Lista para almacenar los elementos del PDF
elements = []

# Definir un estilo para el párrafo
styles = getSampleStyleSheet()
style_normal = styles['Normal']

# Crear una tabla para mostrar todos los resultados en una página
if isinstance(resultados, list) and len(resultados) > 0:
    for item in resultados:
        # Obtener el valor de baseSeverity
        base_severity = item.get("Metrics", {}).get("cvssMetricV31", [{}])[0].get("cvssData", {}).get("baseSeverity", "")

        # Crear una tabla de dos columnas para los datos de cabecera y los valores
        data = [["Dato", "Valor"]]
        data.extend([
            ["Match", item.get("Match", "")],
            ["Plugin", Paragraph(item.get("Plugin", ""),style_normal)],
            ["Version", item.get("Version", "")],
            ["CVE ID", item.get("CVE ID", "")],
            ["CVE Descripcion",Paragraph(item.get("CVE Descripcion", ""), style_normal)],  # Dejar espacio vacío para agregar el párrafo después
            ["Base Severity", base_severity],  # Agregar el valor de Base Severity
        ])

        # Definir el estilo de la tabla
        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
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

        # Agregar el párrafo de CVE Descripcion después de la tabla
        descripcion_paragraph = Paragraph(item.get("CVE Descripcion", ""), style_normal)
        elements.append(PageBreak())  # Salto de página antes de CVE Descripcion
        #elements.append(descripcion_paragraph)

# Construir el PDF
doc.build(elements)

print(f"Todos los resultados se han guardado en {nombre_archivo_pdf}")

