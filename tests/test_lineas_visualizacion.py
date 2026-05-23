from rimador.state import _preparar_lineas_vista, construir_lineas_visualizacion


def _resultados(*textos: str) -> list[dict]:
    return [
        {
            "texto": texto,
            "html_vista_rima": texto,
            "letra_rima": "",
            "color_rima": {
                "background": "transparent",
                "text": "transparent",
                "border": "transparent",
            },
            "posiciones_acentuadas": [],
            "silabas_gramaticales": indice,
            "silabas_metricas": indice,
        }
        for indice, texto in enumerate(textos, start=1)
    ]


def test_construir_lineas_visualizacion_mapea_ultima_linea_activa():
    resultados = _resultados("uno", "dos", "tres")

    assert construir_lineas_visualizacion("uno\ndos\ntres", resultados) == [
        {"texto": "uno", "es_vacia": False, "resultado": resultados[0]},
        {"texto": "dos", "es_vacia": False, "resultado": resultados[1]},
        {"texto": "tres", "es_vacia": False, "resultado": resultados[2]},
    ]


def test_construir_lineas_visualizacion_conserva_salto_final_sin_consumir_resultado():
    resultados = _resultados("uno", "dos", "tres")

    assert construir_lineas_visualizacion("uno\ndos\ntres\n", resultados) == [
        {"texto": "uno", "es_vacia": False, "resultado": resultados[0]},
        {"texto": "dos", "es_vacia": False, "resultado": resultados[1]},
        {"texto": "tres", "es_vacia": False, "resultado": resultados[2]},
        {"texto": "", "es_vacia": True, "resultado": None},
    ]


def test_construir_lineas_visualizacion_no_consume_resultado_en_lineas_vacias():
    resultados = _resultados("uno", "dos")

    assert construir_lineas_visualizacion("uno\n\n dos", resultados) == [
        {"texto": "uno", "es_vacia": False, "resultado": resultados[0]},
        {"texto": "", "es_vacia": True, "resultado": None},
        {"texto": " dos", "es_vacia": False, "resultado": resultados[1]},
    ]


def test_preparar_lineas_vista_muestra_conteo_en_todas_las_lineas_no_vacias():
    lineas = _preparar_lineas_vista(
        "uno\n\n dos\ntres",
        _resultados("uno", "dos", "tres"),
    )

    assert [linea["silabas_gramaticales"] for linea in lineas] == [
        1,
        None,
        2,
        3,
    ]
    assert [linea["silabas_metricas"] for linea in lineas] == [1, None, 2, 3]
