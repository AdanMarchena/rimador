"""Helpers for manually trying the current poetry engine."""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from core.metrica import analizar_metrica_verso
from core.ritmo import obtener_posiciones_acentuadas_verso
from core.rima import (
    clasificar_rima,
    obtener_esquema_rima,
    obtener_ultima_palabra,
    rima_asonante,
    rima_consonante,
)
from core.utils.texto import obtener_versos


def probar_texto(texto: str) -> None:
    """Print verse, metric, word syllable, and rhyme analysis for a text."""
    versos = obtener_versos(texto)

    for numero_verso, verso in enumerate(versos, start=1):
        analisis = analizar_metrica_verso(verso)
        posiciones_acentuadas = obtener_posiciones_acentuadas_verso(verso)

        print(f"Verso {numero_verso}:")
        print(f"Texto: {analisis['verso']}")
        print(f"Sílabas gramaticales: {analisis['silabas_gramaticales']}")
        print(f"Sílabas métricas: {analisis['silabas_metricas']}")
        print(f"Sinalefas: {_formatear_sinalefas(analisis['sinalefas'])}")
        print(f"Ajuste final: {analisis['ajuste_final']}")
        print(f"Posiciones acentuadas: {posiciones_acentuadas}")
        print()

    _mostrar_rimas_entre_versos(versos)
    _mostrar_esquema_rima(versos)


def _mostrar_rimas_entre_versos(versos: list[str]) -> None:
    for indice, (verso_actual, verso_siguiente) in enumerate(
        zip(versos, versos[1:]),
        start=1,
    ):
        palabra_actual = obtener_ultima_palabra(verso_actual)
        palabra_siguiente = obtener_ultima_palabra(verso_siguiente)

        print(f"Rima entre verso {indice} y verso {indice + 1}:")
        print(f"{palabra_actual} / {palabra_siguiente}")
        print(f"Consonante: {_formatear_si_no(rima_consonante(palabra_actual, palabra_siguiente))}")
        print(f"Asonante: {_formatear_si_no(rima_asonante(palabra_actual, palabra_siguiente))}")
        print(f"Tipo de rima: {clasificar_rima(palabra_actual, palabra_siguiente)}")

        if indice < len(versos) - 1:
            print()

    if len(versos) > 1:
        print()


def _mostrar_esquema_rima(versos: list[str]) -> None:
    esquema = obtener_esquema_rima(versos)
    if not esquema:
        return

    print("Esquema de rima:")
    for numero_verso, letra in enumerate(esquema, start=1):
        print(f"Verso {numero_verso}: {letra}")


def _formatear_sinalefas(sinalefas: list[dict]) -> str:
    if not sinalefas:
        return "ninguna"

    return ", ".join(
        f"{sinalefa['anterior']} + {sinalefa['siguiente']}"
        for sinalefa in sinalefas
    )


def _formatear_si_no(valor: bool) -> str:
    return "Sí" if valor else "No"


if __name__ == "__main__":
    texto = """
Escribo esta canción
desde mi corazón
camino sin destino
perdido en el camino
"""
    probar_texto(texto)
