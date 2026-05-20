from core.rima import (
    clasificar_rima,
    obtener_esquema_rima,
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
