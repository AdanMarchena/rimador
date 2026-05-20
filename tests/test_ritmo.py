"""Tests for grammatical rhythmic stress analysis."""

from core.ritmo import obtener_posiciones_acentuadas_verso


def test_obtiene_posiciones_acentuadas_en_verso_con_palabras_llanas():
    assert obtener_posiciones_acentuadas_verso("casa blanca") == [1, 3]


def test_obtiene_posiciones_acentuadas_en_verso_con_agudas_y_monosilaba():
    assert obtener_posiciones_acentuadas_verso("cantar al amor") == [2, 3, 5]


def test_obtiene_posiciones_acentuadas_con_palabra_esdrujula():
    assert obtener_posiciones_acentuadas_verso("p\u00e1jaro azul") == [1, 5]


def test_limpia_puntuacion_basica_al_calcular_posiciones_acentuadas():
    assert obtener_posiciones_acentuadas_verso("\u00a1casa, blanca!") == [1, 3]


def test_verso_vacio_no_tiene_posiciones_acentuadas():
    assert obtener_posiciones_acentuadas_verso("") == []
