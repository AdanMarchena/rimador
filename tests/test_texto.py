from core.utils.texto import obtener_palabras, obtener_versos


def test_obtener_versos_multiples_versos():
    texto = """
Puedo escribir los versos
más tristes esta noche
"""

    assert obtener_versos(texto) == [
        "Puedo escribir los versos",
        "más tristes esta noche",
    ]


def test_obtener_versos_ignora_lineas_vacias():
    texto = """
Hola

mundo


poesía
"""

    assert obtener_versos(texto) == ["Hola", "mundo", "poesía"]


def test_obtener_versos_elimina_espacios_al_inicio_y_final():
    texto = "  primer verso  \n\tsegundo verso\t"

    assert obtener_versos(texto) == ["primer verso", "segundo verso"]


def test_obtener_versos_texto_vacio():
    assert obtener_versos("") == []


def test_obtener_versos_un_solo_verso():
    assert obtener_versos("Un solo verso") == ["Un solo verso"]


def test_obtener_palabras_limpia_puntuacion_basica():
    assert obtener_palabras("\u00bfPuedo escribir?") == ["Puedo", "escribir"]
    assert obtener_palabras('"mi alma",') == ["mi", "alma"]
    assert obtener_palabras("coraz\u00f3n...") == ["coraz\u00f3n"]
    assert obtener_palabras("\u00a1aunque est\u00e9s lejos de m\u00ed!") == [
        "aunque",
        "est\u00e9s",
        "lejos",
        "de",
        "m\u00ed",
    ]


def test_obtener_palabras_conserva_tildes_enie_y_dieresis():
    assert obtener_palabras("\u00a1ni\u00f1o ping\u00fcino!") == [
        "ni\u00f1o",
        "ping\u00fcino",
    ]


def test_obtener_palabras_ignora_tokens_vacios():
    assert obtener_palabras("   ...   \u00bf?   alma   ") == ["alma"]
