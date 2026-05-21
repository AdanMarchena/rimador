"""Responsibility: calculate verse metrics and syllable counts."""

from core.silabeador import separar_silabas_palabra
from core.utils.texto import obtener_palabras

VOCALES = set("aeiou\u00e1\u00e9\u00ed\u00f3\u00fa\u00fcAEIOU\u00c1\u00c9\u00cd\u00d3\u00da\u00dc")
VOCALES_TILDADAS = set("\u00e1\u00e9\u00ed\u00f3\u00fa\u00c1\u00c9\u00cd\u00d3\u00da")


def contar_silabas_gramaticales_verso(verso: str) -> int:
    """Count grammatical syllables in a verse using the current syllabifier."""
    total = 0

    for palabra_limpia in obtener_palabras(verso):
        total += len(separar_silabas_palabra(palabra_limpia))

    return total


def contar_silabas_metricas_verso(verso: str) -> int:
    """Count basic poetic syllables in a verse."""
    return analizar_metrica_verso(verso)["silabas_metricas"]


def resumir_metrica_texto(versos: list[str]) -> dict:
    """Return a compact metric summary for a list of verses."""
    analisis = [analizar_metrica_verso(verso) for verso in versos]
    silabas_metricas = [
        resultado["silabas_metricas"]
        for resultado in analisis
    ]
    tipos_verso = [
        resultado["tipo_verso"]
        for resultado in analisis
    ]

    return {
        "cantidad_versos": len(versos),
        "tipos_verso": tipos_verso,
        "tipo_predominante": _obtener_tipo_predominante(tipos_verso),
        "silabas_metricas_por_verso": silabas_metricas,
        "es_regular": len(set(silabas_metricas)) <= 1,
    }


def analizar_metrica_verso(verso: str) -> dict:
    """Return a detailed basic metric analysis for a verse."""
    palabras = obtener_palabras(verso)
    if not palabras:
        return {
            "verso": verso,
            "silabas_gramaticales": 0,
            "sinalefas": [],
            "cantidad_sinalefas": 0,
            "palabra_final": "",
            "tipo_palabra_final": "",
            "ajuste_final": 0,
            "silabas_metricas": 0,
            "tipo_verso": clasificar_tipo_verso(0),
        }

    silabas_gramaticales = contar_silabas_gramaticales_verso(verso)
    sinalefas = _obtener_sinalefas_basicas(palabras)
    palabra_final = palabras[-1]
    tipo_palabra_final = clasificar_palabra_por_acento(palabra_final)
    ajuste_final = _calcular_ajuste_final(palabras, tipo_palabra_final)
    silabas_metricas = silabas_gramaticales - len(sinalefas) + ajuste_final

    return {
        "verso": verso,
        "silabas_gramaticales": silabas_gramaticales,
        "sinalefas": sinalefas,
        "cantidad_sinalefas": len(sinalefas),
        "palabra_final": palabra_final,
        "tipo_palabra_final": tipo_palabra_final,
        "ajuste_final": ajuste_final,
        "silabas_metricas": silabas_metricas,
        "tipo_verso": clasificar_tipo_verso(silabas_metricas),
    }


def clasificar_tipo_verso(silabas_metricas: int) -> str:
    """Classify a verse by its metric syllable count."""
    tipos = {
        1: "monosílabo",
        2: "bisílabo",
        3: "trisílabo",
        4: "tetrasílabo",
        5: "pentasílabo",
        6: "hexasílabo",
        7: "heptasílabo",
        8: "octosílabo",
        9: "eneasílabo",
        10: "decasílabo",
        11: "endecasílabo",
        12: "dodecasílabo",
        13: "tridecasílabo",
        14: "alejandrino",
    }

    return tipos.get(silabas_metricas, f"verso de {silabas_metricas} sílabas")


def _obtener_tipo_predominante(tipos_verso: list[str]) -> str:
    if not tipos_verso:
        return ""

    return max(tipos_verso, key=lambda tipo: tipos_verso.count(tipo))


def clasificar_palabra_por_acento(palabra: str) -> str:
    """Classify a word as aguda, llana, or esdrujula."""
    palabras = obtener_palabras(palabra)
    palabra_limpia = palabras[0] if palabras else ""
    silabas = separar_silabas_palabra(palabra_limpia)

    for indice, silaba in enumerate(silabas):
        if any(letra in VOCALES_TILDADAS for letra in silaba):
            posicion_desde_final = len(silabas) - indice
            if posicion_desde_final == 1:
                return "aguda"
            if posicion_desde_final == 2:
                return "llana"
            return "esdrujula"

    ultima_letra = palabra_limpia[-1].lower() if palabra_limpia else ""
    if ultima_letra in VOCALES or ultima_letra in {"n", "s"}:
        return "llana"

    return "aguda"


def _contar_sinalefas_basicas(palabras: list[str]) -> int:
    return len(_obtener_sinalefas_basicas(palabras))


def _obtener_sinalefas_basicas(palabras: list[str]) -> list[dict]:
    sinalefas = []

    for palabra_actual, palabra_siguiente in zip(palabras, palabras[1:]):
        if _hay_sinalefa_basica(palabra_actual, palabra_siguiente):
            sinalefas.append(
                {"anterior": palabra_actual, "siguiente": palabra_siguiente}
            )

    return sinalefas


def _calcular_ajuste_final(palabras: list[str], tipo_palabra_final: str) -> int:
    if _ultima_palabra_participa_en_sinalefa(palabras):
        return 0

    if tipo_palabra_final == "aguda":
        return 1
    if tipo_palabra_final == "esdrujula":
        return -1

    return 0


def _hay_sinalefa_basica(palabra_actual: str, palabra_siguiente: str) -> bool:
    if not _empieza_con_vocal_o_h_muda(palabra_siguiente):
        return False

    return _termina_en_vocal(palabra_actual) or palabra_actual.lower() == "el"


def _ultima_palabra_participa_en_sinalefa(palabras: list[str]) -> bool:
    if len(palabras) < 2:
        return False

    return _hay_sinalefa_basica(palabras[-2], palabras[-1])


def _termina_en_vocal(palabra: str) -> bool:
    return bool(palabra) and palabra[-1] in VOCALES


def _empieza_con_vocal_o_h_muda(palabra: str) -> bool:
    if not palabra:
        return False

    palabra_minuscula = palabra.lower()
    return palabra_minuscula[0] in VOCALES or (
        palabra_minuscula.startswith("h")
        and len(palabra_minuscula) > 1
        and palabra_minuscula[1] in VOCALES
    )
