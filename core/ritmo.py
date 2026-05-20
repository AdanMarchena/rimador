"""Responsibility: analyze stress, cadence, and rhythmic structure."""

from core.metrica import clasificar_palabra_por_acento
from core.silabeador import separar_silabas_palabra
from core.utils.texto import obtener_palabras

DISTANCIA_ACENTO_DESDE_FINAL = {
    "aguda": 1,
    "llana": 2,
    "esdrujula": 3,
}


def obtener_posiciones_acentuadas_verso(verso: str) -> list[int]:
    """Return grammatical syllable positions where each word stress falls."""
    posiciones_acentuadas = []
    posicion_inicial_palabra = 1

    for palabra in obtener_palabras(verso):
        silabas = separar_silabas_palabra(palabra)
        if not silabas:
            continue

        tipo_acento = clasificar_palabra_por_acento(palabra)
        distancia_desde_final = DISTANCIA_ACENTO_DESDE_FINAL[tipo_acento]
        indice_silaba_tonica = max(len(silabas) - distancia_desde_final, 0)

        posiciones_acentuadas.append(
            posicion_inicial_palabra + indice_silaba_tonica
        )
        posicion_inicial_palabra += len(silabas)

    return posiciones_acentuadas
