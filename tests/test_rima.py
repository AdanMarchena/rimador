from core.rima import (
    clasificar_rima,
    detectar_rimas_en_texto,
    detectar_rimas_internas,
    obtener_esquema_rima,
    obtener_esquemas_rima_por_estrofa,
    obtener_fragmento_rimante,
    obtener_terminacion_desde_vocal_tonica,
    obtener_ultima_palabra,
    rima_asonante,
    rima_consonante,
)


def test_obtener_ultima_palabra_usa_palabras_limpias():
    assert obtener_ultima_palabra("Puedo escribir,") == "escribir"
    assert obtener_ultima_palabra("\u00bfaunque est\u00e9s lejos de m\u00ed?") == "m\u00ed"
    assert obtener_ultima_palabra("") == ""


def test_obtener_terminacion_desde_vocal_tonica():
    assert obtener_terminacion_desde_vocal_tonica("canci\u00f3n") == "\u00f3n"
    assert obtener_terminacion_desde_vocal_tonica("coraz\u00f3n") == "\u00f3n"
    assert obtener_terminacion_desde_vocal_tonica("camino") == "ino"
    assert obtener_terminacion_desde_vocal_tonica("destino") == "ino"
    assert obtener_terminacion_desde_vocal_tonica("casa") == "asa"
    assert obtener_terminacion_desde_vocal_tonica("brasa") == "asa"


def test_obtener_fragmento_rimante_consonante():
    assert obtener_fragmento_rimante("coraz\u00f3n", "consonante") == "\u00f3n"
    assert obtener_fragmento_rimante("camino", "consonante") == "ino"


def test_obtener_fragmento_rimante_asonante():
    assert obtener_fragmento_rimante("casa", "asonante") == "aa"
    assert obtener_fragmento_rimante("camino", "asonante") == "io"


def test_obtener_fragmento_rimante_sin_rima():
    assert obtener_fragmento_rimante("coraz\u00f3n", "sin_rima") == ""


def test_rima_consonante():
    assert rima_consonante("canci\u00f3n", "coraz\u00f3n") is True
    assert rima_consonante("camino", "destino") is True
    assert rima_consonante("casa", "brasa") is True
    assert rima_consonante("casa", "cama") is False


def test_rima_asonante():
    assert rima_asonante("casa", "rama") is True
    assert rima_asonante("camino", "destino") is True
    assert rima_asonante("canci\u00f3n", "dolor") is False


def test_clasificar_rima():
    assert clasificar_rima("canci\u00f3n", "coraz\u00f3n") == "consonante"
    assert clasificar_rima("casa", "rama") == "asonante"
    assert clasificar_rima("canci\u00f3n", "dolor") == "sin_rima"


def test_detectar_rimas_internas_consonantes():
    assert {
        "palabra": "camino",
        "palabra_final": "destino",
        "tipo": "consonante",
    } in detectar_rimas_internas("camino perdido sin destino")


def test_detectar_rimas_internas_asonantes():
    assert {
        "palabra": "casa",
        "palabra_final": "rama",
        "tipo": "asonante",
    } in detectar_rimas_internas("casa clara sobre la rama")


def test_detectar_rimas_internas_ignora_sin_rima_y_ultima_palabra():
    assert detectar_rimas_internas("noche sin final") == []
    assert detectar_rimas_internas("destino") == []


def test_detectar_rimas_en_texto_detecta_rimas_globales():
    versos = [
        "veamos si algo rima",
        "y me subo a la tarima",
        "no hay cima que pueda conmigo",
        "ni espina ni clima",
    ]

    rimas = detectar_rimas_en_texto(versos)

    assert rimas[0][3] == {
        "palabra": "rima",
        "tipo": "consonante",
        "grupo": "ima",
        "grupo_interno": "ima",
    }
    assert rimas[1][5] == {
        "palabra": "tarima",
        "tipo": "consonante",
        "grupo": "ima",
        "grupo_interno": "ima",
    }
    assert rimas[2][2] == {
        "palabra": "cima",
        "tipo": "consonante",
        "grupo": "ima",
        "grupo_interno": "ima",
    }
    assert rimas[3][3] == {
        "palabra": "clima",
        "tipo": "consonante",
        "grupo": "ima",
        "grupo_interno": "ima",
    }
    assert rimas[3][1] == {
        "palabra": "espina",
        "tipo": "asonante",
        "grupo": "ima",
        "grupo_interno": "asonante:ia",
    }


def test_detectar_rimas_en_texto_asigna_grupos_internos_estables():
    versos = [
        "quiero ser",
        "sin doler",
        "doy manotazo",
        "hachazo",
    ]

    rimas = detectar_rimas_en_texto(versos)

    assert rimas[0][1]["grupo_interno"] == "er"
    assert rimas[1][1]["grupo_interno"] == "er"
    assert rimas[2][1]["grupo_interno"] == "azo"
    assert rimas[3][0]["grupo_interno"] == "azo"
    assert {rimas[0][1]["grupo_interno"], rimas[2][1]["grupo_interno"]} == {
        "er",
        "azo",
    }


def test_detectar_rimas_en_texto_ignora_palabras_funcionales():
    versos = [
        "la rima de la cima",
        "si la tarima ni la espina",
        "de clima ni de rima",
    ]

    rimas = detectar_rimas_en_texto(versos)
    palabras_detectadas = {
        rima["palabra"]
        for rimas_verso in rimas.values()
        for rima in rimas_verso.values()
    }

    assert {"la", "de", "si", "ni"}.isdisjoint(palabras_detectadas)
    assert {"cima", "rima", "tarima", "espina", "clima"} <= palabras_detectadas


def test_obtener_esquema_rima():
    versos = [
        "Escribo esta canci\u00f3n",
        "desde mi coraz\u00f3n",
        "camino sin destino",
        "perdido en el camino",
    ]

    assert obtener_esquema_rima(versos) == ["A", "A", "B", "B"]


def test_obtener_esquema_rima_asigna_nueva_letra_si_no_rima():
    versos = [
        "casa",
        "rama",
        "cielo",
        "flor",
    ]

    assert obtener_esquema_rima(versos) == ["A", "A", "B", "C"]


def test_obtener_esquema_rima_lista_vacia():
    assert obtener_esquema_rima([]) == []


def test_obtener_esquemas_rima_por_estrofa_reinicia_esquema():
    estrofas = [
        [
            "canto con rima",
            "subo a la tarima",
            "camino sin destino",
            "vuelvo por el camino",
        ],
        [
            "cierro la canción",
            "guardo el corazón",
            "miro la casa",
            "cruzo por la brasa",
        ],
    ]

    assert obtener_esquemas_rima_por_estrofa(estrofas) == [
        {
            "estrofa": 1,
            "versos": estrofas[0],
            "esquema": ["A", "A", "B", "B"],
            "esquema_texto": "AABB",
        },
        {
            "estrofa": 2,
            "versos": estrofas[1],
            "esquema": ["A", "A", "B", "B"],
            "esquema_texto": "AABB",
        },
    ]


def test_obtener_esquemas_rima_por_estrofa_no_mezcla_estrofas():
    estrofas = [
        ["casa", "flor"],
        ["brasa", "calor"],
    ]

    assert obtener_esquemas_rima_por_estrofa(estrofas) == [
        {
            "estrofa": 1,
            "versos": ["casa", "flor"],
            "esquema": ["A", "B"],
            "esquema_texto": "AB",
        },
        {
            "estrofa": 2,
            "versos": ["brasa", "calor"],
            "esquema": ["A", "B"],
            "esquema_texto": "AB",
        },
    ]
