"""PDF export for analysis results."""

from io import BytesIO

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer


def generar_pdf_analisis(texto: str, resultados: list[dict], resumen: dict) -> bytes:
    """Generate a PDF document with the complete text analysis."""
    buffer = BytesIO()
    documento = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=48,
        leftMargin=48,
        topMargin=48,
        bottomMargin=48,
    )
    estilos = getSampleStyleSheet()
    elementos = [
        Paragraph("Rimador - Análisis del texto", estilos["Title"]),
        Spacer(1, 12),
        Paragraph("Texto original", estilos["Heading2"]),
        Paragraph(_lineas_a_html(texto or "Sin texto ingresado."), estilos["BodyText"]),
        Spacer(1, 12),
        Paragraph("Resumen general", estilos["Heading2"]),
    ]

    for etiqueta, valor in _items_resumen(resumen):
        elementos.append(Paragraph(f"<b>{etiqueta}:</b> {_escapar(valor)}", estilos["BodyText"]))

    elementos.extend(
        [
            Spacer(1, 12),
            Paragraph("Análisis verso a verso", estilos["Heading2"]),
        ]
    )

    if not resultados:
        elementos.append(Paragraph("No hay versos analizados.", estilos["BodyText"]))
    else:
        for indice, resultado in enumerate(resultados, start=1):
            elementos.extend(_bloque_verso(indice, resultado, estilos))

    documento.build(elementos)
    return buffer.getvalue()


def _items_resumen(resumen: dict) -> list[tuple[str, str]]:
    esquemas = resumen.get("esquemas_rima", [])
    esquemas_texto = "; ".join(
        f"{item.get('etiqueta', '')}: {item.get('esquema', '')}".strip()
        for item in esquemas
    ) or "Sin esquema"

    return [
        ("Versos totales", str(resumen.get("versos_totales", 0))),
        ("Estrofas", str(resumen.get("estrofas", 0))),
        ("Métrica predominante", resumen.get("metrica_predominante", "Sin versos")),
        ("Regularidad", resumen.get("regularidad", "regular")),
        ("Esquemas de rima", esquemas_texto),
    ]


def _bloque_verso(indice: int, resultado: dict, estilos) -> list:
    return [
        Spacer(1, 8),
        Paragraph(f"Verso {indice}: {_escapar(resultado.get('texto', ''))}", estilos["Heading3"]),
        Paragraph(
            f"<b>Sílabas gramaticales:</b> {_escapar(resultado.get('silabas_gramaticales', ''))}",
            estilos["BodyText"],
        ),
        Paragraph(
            f"<b>Sílabas métricas:</b> {_escapar(resultado.get('silabas_metricas', ''))}",
            estilos["BodyText"],
        ),
        Paragraph(
            f"<b>Tipo de verso:</b> {_escapar(resultado.get('tipo_verso', ''))}",
            estilos["BodyText"],
        ),
        Paragraph(
            f"<b>Sinalefas:</b> {_escapar(resultado.get('sinalefas', ''))}",
            estilos["BodyText"],
        ),
        Paragraph(
            f"<b>Ajuste final:</b> {_escapar(resultado.get('ajuste_final', ''))}",
            estilos["BodyText"],
        ),
        Paragraph(
            f"<b>Rima final:</b> {_escapar(resultado.get('letra_rima', ''))} "
            f"({_escapar(resultado.get('tipo_rima', ''))})",
            estilos["BodyText"],
        ),
    ]


def _lineas_a_html(texto: str) -> str:
    return "<br/>".join(_escapar(linea) for linea in texto.splitlines()) or "Sin texto ingresado."


def _escapar(valor) -> str:
    return (
        str(valor)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )
