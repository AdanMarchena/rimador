from core.utils.texto import obtener_versos


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
