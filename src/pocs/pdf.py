import os
import json
import datetime
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, PageBreak, Paragraph, Spacer, FrameBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus.frames import Frame

class GeneradorPDF:
    def __init__(self, ruta_archivo_json):
        self.ruta_archivo_json = ruta_archivo_json
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

    def generar_pdf(self, nombre_archivo_pdf):
        fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        doc = SimpleDocTemplate(
            nombre_archivo_pdf,
            pagesize=landscape(letter),
            leftMargin=20,
            rightMargin=20,
        )
        elements = []
        styles = getSampleStyleSheet()
        custom_style = ParagraphStyle(name='CustomTitle', fontSize=24, alignment=1)
        styles.add(custom_style)
        style_normal = styles['Normal']
        title = f"Resultados de evaluación - Fecha: {fecha_actual}"
        elements.append(Paragraph(title, custom_style))
        elements.append(Spacer(1, 20))
        if isinstance(self.resultados, list) and len(self.resultados) > 0:
            for item in self.resultados:
                data = [["Dato", "Valor"]]
                data.extend([
                    ["Match", Paragraph(item.get("Match", ""), style_normal)],
                    ["Plugin", Paragraph(item.get("Plugin", ""), style_normal)],
                    ["Version", Paragraph(item.get("Version", ""), style_normal)],
                    ["CVE ID", Paragraph(item.get("CVE ID", ""), style_normal)],
                    ["CVE Descripcion", Paragraph(item.get("CVE Descripcion", ""), style_normal)],
                    ["Severidad", item.get("Metrics", {}).get("cvssMetricV31", [{}])[0].get("cvssData", {}).get("baseSeverity", "")],
                ])
                table_style = TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Alineación vertical al centro
                ])

                elements.append(Spacer(1, 100))  # Espacio en blanco para centrar verticalmente
                tabla = Table(data, colWidths=[150, None])
                tabla.setStyle(table_style)
                elements.append(tabla)
                elements.append(FrameBreak())

        doc.build(elements)
        print(f"Todos los resultados se han guardado en {nombre_archivo_pdf}")

if __name__ == "__main__":
    ruta_archivo_json = "resultados.json"
    nombre_archivo_pdf = f"reportes/resultados_escaneo_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.pdf"
    generador_pdf = GeneradorPDF(ruta_archivo_json)
    generador_pdf.generar_pdf(nombre_archivo_pdf)
