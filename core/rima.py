"""Responsibility: detect and classify rhyme patterns."""

from core.data.palabras_excluidas import PALABRAS_EXCLUIDAS_RIMA
from core.silabeador import separar_silabas_palabra
from core.utils.texto import obtener_palabras

VOCALES = set("aeiou\u00e1\u00e9\u00ed\u00f3\u00fa\u00fcAEIOU\u00c1\u00c9\u00cd\u00d3\u00da\u00dc")
VOCALES_TILDADAS = set("\u00e1\u00e9\u00ed\u00f3\u00fa\u00c1\u00c9\u00cd\u00d3\u00da")
MAPA_SIN_TILDES = str.maketrans(
    "\u00e1\u00e9\u00ed\u00f3\u00fa\u00fc\u00c1\u00c9\u00cd\u00d3\u00da\u00dc",
    "aeiouuAEIOUU",
)


def obtener_ultima_palabra(verso: str) -> str:
    """Return the last clean word from a verse."""
    palabras = obtener_palabras(verso)
    return palabras[-1] if palabras else ""


def obtener_terminacion_desde_vocal_tonica(palabra: str) -> str:
    """Return the word ending from the stressed vowel onward."""
    palabras = obtener_palabras(palabra)
    palabra_limpia = palabras[0] if palabras else ""
    if not palabra_limpia:
        return ""

    indice_tonico = _obtener_indice_vocal_tonica(palabra_limpia)
    return palabra_limpia[indice_tonico:]


def obtener_fragmento_rimante(palabra: str, tipo: str) -> str:
    """Return the rhyming fragment for a word and rhyme type."""
    if tipo == "sin_rima":
        return ""

    terminacion = obtener_terminacion_desde_vocal_tonica(palabra)
    if tipo == "consonante":
        return terminacion

    if tipo == "asonante":
        return _obtener_vocales_normalizadas(terminacion)

    return ""


def rima_consonante(palabra1: str, palabra2: str) -> bool:
    """Return whether two words have consonant rhyme."""
    terminacion1 = _normalizar(obtener_terminacion_desde_vocal_tonica(palabra1))
    terminacion2 = _normalizar(obtener_terminacion_desde_vocal_tonica(palabra2))

    return bool(terminacion1) and terminacion1 == terminacion2


def rima_asonante(palabra1: str, palabra2: str) -> bool:
    """Return whether two words have assonant rhyme."""
    vocales1 = _obtener_vocales_normalizadas(
        obtener_terminacion_desde_vocal_tonica(palabra1)
    )
    vocales2 = _obtener_vocales_normalizadas(
        obtener_terminacion_desde_vocal_tonica(palabra2)
    )

    return bool(vocales1) and vocales1 == vocales2


def clasificar_rima(palabra1: str, palabra2: str) -> str:
    """Classify the rhyme between two words."""
    if rima_consonante(palabra1, palabra2):
        return "consonante"

    if rima_asonante(palabra1, palabra2):
        return "asonante"

    return "sin_rima"


def detectar_rimas_internas(verso: str) -> list[dict]:
    """Detect words inside a verse that rhyme with its final word."""
    palabras = obtener_palabras(verso)
    if len(palabras) < 2:
        return []

    palabra_final = palabras[-1]
    rimas = []

    for palabra in palabras[:-1]:
        tipo = clasificar_rima(palabra, palabra_final)
        if tipo in {"consonante", "asonante"}:
            rimas.append(
                {
                    "palabra": palabra,
                    "palabra_final": palabra_final,
                    "tipo": tipo,
                }
            )

    return rimas


def detectar_rimas_en_texto(versos: list[str]) -> dict:
    """Detect rhyming words across a full text."""
    palabras = _obtener_palabras_indexadas(versos)
    rimas: dict[int, dict[int, dict]] = {}

    for palabra_actual in palabras:
        coincidencias = []

        for otra_palabra in palabras:
            if palabra_actual is otra_palabra:
                continue

            tipo = clasificar_rima(
                palabra_actual["palabra"],
                otra_palabra["palabra"],
            )
            if tipo == "sin_rima":
                continue

            coincidencias.append(
                {
                    "tipo": tipo,
                    "grupo": obtener_fragmento_rimante(
                        otra_palabra["palabra"],
                        tipo,
                    ),
                    "palabra": otra_palabra["palabra"],
                }
            )

        if not coincidencias:
            continue

        mejor_tipo = _mejor_tipo_rima(coincidencias)
        grupo = _mejor_grupo_rima(palabra_actual["palabra"], mejor_tipo, coincidencias)
        indice_verso = palabra_actual["indice_verso"]
        indice_palabra = palabra_actual["indice_palabra"]

        rimas.setdefault(indice_verso, {})[indice_palabra] = {
            "palabra": palabra_actual["palabra"],
            "tipo": mejor_tipo,
            "grupo": grupo,
            "grupo_interno": _obtener_grupo_interno(
                palabra_actual["palabra"],
                mejor_tipo,
            ),
        }

    return rimas


def obtener_esquema_rima(versos: list[str]) -> list[str]:
    """Assign rhyme scheme letters to a list of verses."""
    esquema = []
    palabras_finales = []

    for verso in versos:
        palabra_actual = obtener_ultima_palabra(verso)
        letra = _buscar_letra_de_rima(palabra_actual, palabras_finales, esquema)

        if letra is None:
            letra = _letra_de_esquema(len(set(esquema)))

        palabras_finales.append(palabra_actual)
        esquema.append(letra)

    return esquema


def _obtener_palabras_indexadas(versos: list[str]) -> list[dict]:
    palabras_indexadas = []

    for indice_verso, verso in enumerate(versos):
        for indice_palabra, palabra in enumerate(obtener_palabras(verso)):
            palabra_normalizada = _normalizar(palabra)
            if (
                len(palabra_normalizada) <= 2
                or palabra_normalizada in PALABRAS_EXCLUIDAS_RIMA
            ):
                continue

            palabras_indexadas.append(
                {
                    "palabra": palabra,
                    "indice_verso": indice_verso,
                    "indice_palabra": indice_palabra,
                }
            )

    return palabras_indexadas


def _mejor_tipo_rima(coincidencias: list[dict]) -> str:
    if any(coincidencia["tipo"] == "consonante" for coincidencia in coincidencias):
        return "consonante"

    return "asonante"


def _mejor_grupo_rima(
    palabra: str,
    tipo: str,
    coincidencias: list[dict],
) -> str:
    grupo_propio = obtener_fragmento_rimante(palabra, tipo)
    if tipo == "consonante":
        return grupo_propio

    grupos_consonantes = [
        obtener_fragmento_rimante(coincidencia["palabra"], "consonante")
        for coincidencia in coincidencias
        if coincidencia["grupo"] == grupo_propio
    ]
    grupos_consonantes = [grupo for grupo in grupos_consonantes if grupo]
    if grupos_consonantes:
        return _grupo_mas_frecuente(grupos_consonantes)

    return grupo_propio


def _obtener_grupo_interno(palabra: str, tipo: str) -> str:
    if tipo == "consonante":
        return obtener_fragmento_rimante(palabra, "consonante")

    if tipo == "asonante":
        return f"asonante:{obtener_fragmento_rimante(palabra, 'asonante')}"

    return ""


def _grupo_mas_frecuente(grupos: list[str]) -> str:
    return max(grupos, key=lambda grupo: (grupos.count(grupo), len(grupo)))


def _obtener_indice_vocal_tonica(palabra: str) -> int:
    for indice, letra in enumerate(palabra):
        if letra in VOCALES_TILDADAS:
            return indice

    silabas = separar_silabas_palabra(palabra)
    if not silabas:
        return 0

    indice_silaba_tonica = _obtener_indice_silaba_tonica_sin_tilde(palabra, silabas)
    inicio_silaba = sum(len(silaba) for silaba in silabas[:indice_silaba_tonica])

    for indice in range(inicio_silaba, len(palabra)):
        if palabra[indice] in VOCALES:
            return indice

    return inicio_silaba


def _buscar_letra_de_rima(
    palabra_actual: str,
    palabras_finales: list[str],
    esquema: list[str],
) -> str | None:
    for palabra_anterior, letra_anterior in zip(palabras_finales, esquema):
        if clasificar_rima(palabra_actual, palabra_anterior) != "sin_rima":
            return letra_anterior

    return None


def _letra_de_esquema(indice: int) -> str:
    letras = []

    while True:
        letras.append(chr(ord("A") + indice % 26))
        indice = indice // 26 - 1
        if indice < 0:
            break

    return "".join(reversed(letras))


def _obtener_indice_silaba_tonica_sin_tilde(palabra: str, silabas: list[str]) -> int:
    ultima_letra = palabra[-1].lower()
    if ultima_letra in VOCALES or ultima_letra in {"n", "s"}:
        return max(len(silabas) - 2, 0)

    return len(silabas) - 1


def _normalizar(texto: str) -> str:
    return texto.translate(MAPA_SIN_TILDES).lower()


def _obtener_vocales_normalizadas(texto: str) -> str:
    return "".join(letra.lower() for letra in texto if letra in VOCALES)
