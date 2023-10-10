import os
import json
import datetime
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, PageBreak, Paragraph, Image, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

class GeneradorPDF:
    def __init__(self, ruta_archivo_json, nombre_archivo_pdf):
        self.ruta_archivo_json = ruta_archivo_json
        self.nombre_archivo_pdf = nombre_archivo_pdf
        self.resultados = self.cargar_resultados_desde_archivo()

    def cargar_resultados_desde_archivo(self):
        try:
            with open(self.ruta_archivo_json, 'r') as archivo:
                data = json.load(archivo)
                return data
        except FileNotFoundError:
            return "El archivo no fue encontrado"
        except json.JSONDecodeError:
            return "Error al analizar el JSON del archivo"

    def generar_pdf(self):
        # Obtener la fecha actual
        fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d-H%-M%-S%")

        # Crear la carpeta 'reportes' si no existe
        carpeta_reportes = os.path.dirname(self.nombre_archivo_pdf)
        if not os.path.exists(carpeta_reportes):
            os.makedirs(carpeta_reportes)

        # Crear un documento PDF con tamaño de hoja en carta (8.5 x 11 pulgadas) y orientación horizontal
        doc = SimpleDocTemplate(self.nombre_archivo_pdf, pagesize=landscape(letter), leftMargin=20, rightMargin=20)

        # Lista para almacenar los elementos del PDF
        elements = []

        # Definir un estilo para el título
        styles = getSampleStyleSheet()
        style_title = styles['Title']
        style_title.alignment = 1  # Centrar el título
        style_title.fontName = 'Helvetica-Bold'  # Usar negrita para el título

        # Agregar el título "Resultados de Evaluación"
        titulo = Paragraph("<b>Resultados de Evaluación</b>", style_title)
        elements.append(titulo)

        # Agregar una línea en blanco
        elements.append(Spacer(1, 12))  # Espacio en blanco de 12 puntos

        # Crear una tabla para mostrar todos los resultados en una página
        if isinstance(self.resultados, list) and len(self.resultados) > 0:
            data = [["Dato", "Valor"]]
            for item in self.resultados:
                # Obtener el valor de baseSeverity
                base_severity = item.get("Metrics", {}).get("cvssMetricV31", [{}])[0].get("cvssData", {}).get("baseSeverity", "")

                # Agregar los datos a la tabla
                data.append(["Match", item.get("Match", "")])
                data.append(["Plugin", item.get("Plugin", "")])
                data.append(["Version", item.get("Version", "")])
                data.append(["CVE ID", item.get("CVE ID", "")])
                data.append(["CVE Descripcion", item.get("CVE Descripcion", "")])
                data.append(["Severidad", base_severity])

            # Definir el estilo de la tabla
            table_style = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ])

            # Aumentar el ancho de la columna "Valor" para que se ajuste al contenido
            col_widths = [150, None]

            # Crear la tabla y aplicar el estilo
            tabla = Table(data, colWidths=col_widths)
            tabla.setStyle(table_style)

            # Agregar la tabla al documento
            elements.append(tabla)

        # Construir el PDF
        doc.build(elements)

        print(f"Todos los resultados se han guardado en {self.nombre_archivo_pdf}")

if __name__ == "__main__":
    # Rutas relativas
    ruta_archivo_json = "resultados.json"
    carpeta_reportes = "reportes"
    fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    nombre_archivo_pdf = os.path.join(carpeta_reportes, f"resultados_escaneo_{fecha_actual}.pdf")

    generador_pdf = GeneradorPDF(ruta_archivo_json, nombre_archivo_pdf)
    generador_pdf.generar_pdf()

