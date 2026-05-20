"""Responsibility: split Spanish words into syllables."""

VOCALES = set("aeiouáéíóúüAEIOUÁÉÍÓÚÜ")
VOCALES_FUERTES = set("aeoáéóAEOÁÉÓ")
VOCALES_DEBILES = set("iuüIUÜ")
VOCALES_DEBILES_TILDADAS = set("íúÍÚ")
GRUPOS_CONSONANTICOS = {
    "pl",
    "pr",
    "bl",
    "br",
    "cl",
    "cr",
    "dr",
    "fl",
    "fr",
    "gl",
    "gr",
    "tl",
    "tr",
}
DIGRAFOS_CONSONANTICOS = {"ch", "ll", "rr"}


def separar_silabas_palabra(palabra: str) -> list[str]:
    """Separate a single Spanish word into a first-pass syllable list.

    This initial syllabifier handles simple vowels, basic diphthongs, hiatus
    caused by accented weak vowels, and frequent consonant clusters. It does
    not handle verse-level phenomena such as sinalefa or metric syllables.
    """
    palabra = palabra.strip()
    if not palabra:
        return []

    nucleos = _obtener_nucleos_vocalicos(palabra)
    if not nucleos:
        return [palabra]

    silabas = []
    inicio = 0

    for indice, (nucleo_inicio, nucleo_fin) in enumerate(nucleos[:-1]):
        siguiente_inicio = nucleos[indice + 1][0]
        consonantes = palabra[nucleo_fin + 1 : siguiente_inicio]
        corte = _calcular_corte(
            nucleo_fin=nucleo_fin,
            siguiente_inicio=siguiente_inicio,
            consonantes=consonantes,
        )
        silabas.append(palabra[inicio:corte])
        inicio = corte

    silabas.append(palabra[inicio:])
    return silabas


def _obtener_nucleos_vocalicos(palabra: str) -> list[tuple[int, int]]:
    nucleos = []
    indice = 0

    while indice < len(palabra):
        if not _es_vocal(palabra[indice]):
            indice += 1
            continue

        inicio = indice
        fin = indice
        indice += 1

        while indice < len(palabra) and _es_vocal(palabra[indice]):
            if _forman_diptongo(palabra[fin], palabra[indice]):
                fin = indice
                indice += 1
                continue
            break

        nucleos.append((inicio, fin))

    return nucleos


def _calcular_corte(
    nucleo_fin: int,
    siguiente_inicio: int,
    consonantes: str,
) -> int:
    if not consonantes:
        return nucleo_fin + 1

    if len(consonantes) == 1:
        return siguiente_inicio - 1

    if consonantes[-2:].lower() in GRUPOS_CONSONANTICOS | DIGRAFOS_CONSONANTICOS:
        return siguiente_inicio - 2

    return siguiente_inicio - 1


def _forman_diptongo(primera: str, segunda: str) -> bool:
    if primera in VOCALES_DEBILES_TILDADAS or segunda in VOCALES_DEBILES_TILDADAS:
        return False

    primera_es_debil = primera in VOCALES_DEBILES
    segunda_es_debil = segunda in VOCALES_DEBILES
    primera_es_fuerte = primera in VOCALES_FUERTES
    segunda_es_fuerte = segunda in VOCALES_FUERTES

    return (
        primera_es_debil
        and segunda_es_debil
        or primera_es_debil
        and segunda_es_fuerte
        or primera_es_fuerte
        and segunda_es_debil
    )


def _es_vocal(letra: str) -> bool:
    return letra in VOCALES
