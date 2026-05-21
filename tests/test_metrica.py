"""Tests for metric analysis behavior."""

from core.metrica import (
    analizar_metrica_verso,
    clasificar_palabra_por_acento,
    clasificar_tipo_verso,
    contar_silabas_gramaticales_verso,
    contar_silabas_metricas_verso,
    resumir_metrica_texto,
)


def test_cuenta_silabas_gramaticales_en_versos_simples():
    assert contar_silabas_gramaticales_verso("casa blanca") == 4
    assert contar_silabas_gramaticales_verso("pueblo triste") == 4
    assert contar_silabas_gramaticales_verso("Puedo escribir") == 5
    assert contar_silabas_gramaticales_verso(
        "los versos m\u00e1s tristes esta noche"
    ) == 10


def test_limpia_puntuacion_basica_al_inicio_y_final():
    assert contar_silabas_gramaticales_verso("\u00a1casa, blanca!") == 4


def test_clasifica_palabras_por_acento():
    assert clasificar_palabra_por_acento("amor") == "aguda"
    assert clasificar_palabra_por_acento("canci\u00f3n") == "aguda"
    assert clasificar_palabra_por_acento("casa") == "llana"
    assert clasificar_palabra_por_acento("verso") == "llana"
    assert clasificar_palabra_por_acento("m\u00fasica") == "esdrujula"
    assert clasificar_palabra_por_acento("p\u00e1jaro") == "esdrujula"


def test_clasifica_tipo_verso():
    assert clasificar_tipo_verso(1) == "monosílabo"
    assert clasificar_tipo_verso(2) == "bisílabo"
    assert clasificar_tipo_verso(3) == "trisílabo"
    assert clasificar_tipo_verso(4) == "tetrasílabo"
    assert clasificar_tipo_verso(5) == "pentasílabo"
    assert clasificar_tipo_verso(6) == "hexasílabo"
    assert clasificar_tipo_verso(7) == "heptasílabo"
    assert clasificar_tipo_verso(8) == "octosílabo"
    assert clasificar_tipo_verso(9) == "eneasílabo"
    assert clasificar_tipo_verso(10) == "decasílabo"
    assert clasificar_tipo_verso(11) == "endecasílabo"
    assert clasificar_tipo_verso(12) == "dodecasílabo"
    assert clasificar_tipo_verso(13) == "tridecasílabo"
    assert clasificar_tipo_verso(14) == "alejandrino"
    assert clasificar_tipo_verso(15) == "verso de 15 sílabas"


def test_cuenta_silabas_metricas_con_sinalefa_basica():
    assert contar_silabas_gramaticales_verso("mi alma") == 3
    assert contar_silabas_metricas_verso("mi alma") == 2
    assert contar_silabas_gramaticales_verso("la estrella") == 4
    assert contar_silabas_metricas_verso("la estrella") == 3
    assert contar_silabas_metricas_verso("canta el alma") == 3
    assert contar_silabas_gramaticales_verso("de oro") == 3
    assert contar_silabas_metricas_verso("de oro") == 2
    assert contar_silabas_metricas_verso("la humilde casa") == 5


def test_sinalefa_entre_vocales_simples():
    assert contar_silabas_gramaticales_verso("Puedo escribir") == 5
    assert contar_silabas_metricas_verso("Puedo escribir") == 4


def test_sinalefa_con_h_muda_seguida_de_vocal():
    assert contar_silabas_gramaticales_verso("su herida") == 4
    assert contar_silabas_metricas_verso("su herida") == 3


def test_cuenta_silabas_metricas_con_palabra_final_aguda():
    assert contar_silabas_metricas_verso("gran amor") == 4
    assert contar_silabas_metricas_verso("mi canci\u00f3n") == 4


def test_cuenta_silabas_metricas_con_palabra_final_llana():
    assert contar_silabas_metricas_verso("casa blanca") == 4


def test_cuenta_silabas_metricas_con_palabra_final_esdrujula():
    assert contar_silabas_metricas_verso("la m\u00fasica") == 3


def test_analiza_metrica_detallada_de_verso():
    assert analizar_metrica_verso("aunque est\u00e9s lejos de m\u00ed") == {
        "verso": "aunque est\u00e9s lejos de m\u00ed",
        "silabas_gramaticales": 8,
        "sinalefas": [{"anterior": "aunque", "siguiente": "est\u00e9s"}],
        "cantidad_sinalefas": 1,
        "palabra_final": "m\u00ed",
        "tipo_palabra_final": "aguda",
        "ajuste_final": 1,
        "silabas_metricas": 8,
        "tipo_verso": "octosílabo",
    }


def test_analiza_metrica_con_ultima_palabra_en_sinalefa():
    analisis = analizar_metrica_verso("Puedo escribir")

    assert analisis["silabas_gramaticales"] == 5
    assert analisis["sinalefas"] == [
        {"anterior": "Puedo", "siguiente": "escribir"}
    ]
    assert analisis["cantidad_sinalefas"] == 1
    assert analisis["palabra_final"] == "escribir"
    assert analisis["tipo_palabra_final"] == "aguda"
    assert analisis["ajuste_final"] == 0
    assert analisis["silabas_metricas"] == 4
    assert analisis["tipo_verso"] == "tetrasílabo"


def test_analiza_metrica_con_sinalefa_y_palabra_final_llana():
    assert analizar_metrica_verso("la estrella") == {
        "verso": "la estrella",
        "silabas_gramaticales": 4,
        "sinalefas": [{"anterior": "la", "siguiente": "estrella"}],
        "cantidad_sinalefas": 1,
        "palabra_final": "estrella",
        "tipo_palabra_final": "llana",
        "ajuste_final": 0,
        "silabas_metricas": 3,
        "tipo_verso": "trisílabo",
    }


def test_resume_metrica_texto_regular():
    resumen = resumir_metrica_texto([
        "casa blanca",
        "pueblo triste",
    ])

    assert resumen == {
        "cantidad_versos": 2,
        "tipos_verso": ["tetrasílabo", "tetrasílabo"],
        "tipo_predominante": "tetrasílabo",
        "silabas_metricas_por_verso": [4, 4],
        "es_regular": True,
    }


def test_resume_metrica_texto_irregular_y_predominante():
    resumen = resumir_metrica_texto([
        "casa blanca",
        "la estrella",
        "Puedo escribir",
    ])

    assert resumen["cantidad_versos"] == 3
    assert resumen["tipos_verso"] == ["tetrasílabo", "trisílabo", "tetrasílabo"]
    assert resumen["tipo_predominante"] == "tetrasílabo"
    assert resumen["silabas_metricas_por_verso"] == [4, 3, 4]
    assert resumen["es_regular"] is False


def test_resume_metrica_texto_vacio():
    assert resumir_metrica_texto([]) == {
        "cantidad_versos": 0,
        "tipos_verso": [],
        "tipo_predominante": "",
        "silabas_metricas_por_verso": [],
        "es_regular": True,
    }
