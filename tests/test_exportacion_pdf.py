from core.exportacion.pdf import generar_pdf_analisis


def test_generar_pdf_analisis_devuelve_pdf():
    pdf = generar_pdf_analisis(
        "canto con rima",
        [
            {
                "texto": "canto con rima",
                "silabas_gramaticales": 5,
                "silabas_metricas": 5,
                "tipo_verso": "pentasílabo",
                "arte_verso": "arte menor",
                "sinalefas": "Sin sinalefas",
                "ajuste_final": "0 por palabra llana",
                "letra_rima": "A",
                "tipo_rima": "sin_rima",
            }
        ],
        {
            "versos_totales": 1,
            "estrofas": 1,
            "metrica_predominante": "pentasílabo",
            "regularidad": "regular",
            "esquemas_rima": [{"etiqueta": "Estrofa 1", "esquema": "A"}],
        },
    )

    assert pdf.startswith(b"%PDF")
    assert len(pdf) > 1000
