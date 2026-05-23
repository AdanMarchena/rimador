"""Responsibility: detect and classify rhyme patterns."""

from core.data.palabras_excluidas import PALABRAS_EXCLUIDAS_RIMA
from core.silabeador import separar_silabas_palabra
from core.utils.texto import obtener_palabras

VOCALES = set("aeiou\u00e1\u00e9\u00ed\u00f3\u00fa\u00fcAEIOU\u00c1\u00c9\u00cd\u00d3\u00da\u00dc")
VOCALES_TILDADAS = set("\u00e1\u00e9\u00ed\u00f3\u00fa\u00c1\u00c9\u00cd\u00d3\u00da")
VOCALES_FUERTES = set("aeo\u00e1\u00e9\u00f3AEO\u00c1\u00c9\u00d3")
VOCALES_DEBILES = set("iu\u00fcIU\u00dc")
VOCALES_DEBILES_TILDADAS = set("\u00ed\u00fa\u00cd\u00da")
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
        return obtener_clave_asonante(palabra)

    return ""


def rima_consonante(palabra1: str, palabra2: str) -> bool:
    """Return whether two words have consonant rhyme."""
    terminacion1 = _normalizar(obtener_terminacion_desde_vocal_tonica(palabra1))
    terminacion2 = _normalizar(obtener_terminacion_desde_vocal_tonica(palabra2))

    return bool(terminacion1) and terminacion1 == terminacion2


def rima_asonante(palabra1: str, palabra2: str) -> bool:
    """Return whether two words have assonant rhyme."""
    vocales1 = obtener_clave_asonante(palabra1)
    vocales2 = obtener_clave_asonante(palabra2)

    return bool(vocales1) and vocales1 == vocales2


def obtener_clave_asonante(palabra: str) -> str:
    """Return the normalized assonant key for a word."""
    palabras = obtener_palabras(palabra)
    palabra_limpia = palabras[0] if palabras else ""
    if not palabra_limpia:
        return ""

    nucleos = _obtener_nucleos_vocalicos_asonantes(palabra_limpia)
    if not nucleos:
        return ""

    indice_tonico = _obtener_indice_vocal_tonica(palabra_limpia)
    indice_nucleo_tonico = _obtener_indice_nucleo_por_posicion(nucleos, indice_tonico)
    vocales = [
        _vocal_representativa_asonante(palabra_limpia, nucleo)
        for nucleo in nucleos[indice_nucleo_tonico:]
    ]

    if _es_esdrujula(palabra_limpia) and len(vocales) > 1:
        vocales = [vocales[0], vocales[-1]]

    return "".join(vocales)


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
        if tipo == "asonante" and not _tienen_clave_asonante_fuerte(
            palabra,
            palabra_final,
        ):
            continue

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
            if tipo == "asonante" and not _tienen_clave_asonante_fuerte(
                palabra_actual["palabra"],
                otra_palabra["palabra"],
            ):
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


def agrupar_rimas_por_estrofa(estrofas: list[list[str]]) -> list[dict]:
    """Group relevant rhyme networks independently in each stanza."""
    grupos_por_estrofa = []

    for indice_estrofa, estrofa in enumerate(estrofas, start=1):
        palabras = _obtener_palabras_unicas_estrofa(estrofa)
        palabras_finales = {
            _normalizar(ultima_palabra)
            for verso in estrofa
            if (ultima_palabra := obtener_ultima_palabra(verso))
        }
        palabras_repetidas = _obtener_palabras_repetidas_estrofa(estrofa)
        palabras_con_consonante = set()
        grupos = []

        for clave, palabras_grupo in _agrupar_palabras_por_fragmento(
            palabras,
            "consonante",
        ).items():
            if len(palabras_grupo) < 2:
                continue
            if not _grupo_relevante_para_resumen(
                palabras_grupo,
                palabras_finales,
                palabras_repetidas,
            ):
                continue

            grupos.append(
                {
                    "tipo": "consonante",
                    "clave": clave,
                    "palabras": palabras_grupo,
                }
            )
            palabras_con_consonante.update(
                _normalizar(palabra) for palabra in palabras_grupo
            )

        palabras_asonantes = [
            palabra
            for palabra in palabras
            if _normalizar(palabra) not in palabras_con_consonante
        ]
        for clave, palabras_grupo in _agrupar_palabras_por_fragmento(
            palabras_asonantes,
            "asonante",
        ).items():
            if len(clave) < 2 or len(palabras_grupo) < 2:
                continue
            if not _grupo_relevante_para_resumen(
                palabras_grupo,
                palabras_finales,
                palabras_repetidas,
            ):
                continue

            grupos.append(
                {
                    "tipo": "asonante",
                    "clave": clave,
                    "palabras": palabras_grupo,
                }
            )

        grupos_por_estrofa.append(
            {
                "estrofa": indice_estrofa,
                "grupos": [
                    {
                        "grupo": _letra_de_esquema(indice),
                        **grupo,
                    }
                    for indice, grupo in enumerate(grupos)
                ],
            }
        )

    return grupos_por_estrofa


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


def obtener_esquemas_rima_por_estrofa(estrofas: list[list[str]]) -> list[dict]:
    """Return rhyme schemes independently for each stanza."""
    return [
        {
            "estrofa": indice + 1,
            "versos": estrofa,
            "esquema": esquema,
            "esquema_texto": "".join(esquema),
        }
        for indice, estrofa in enumerate(estrofas)
        if (esquema := obtener_esquema_rima(estrofa))
    ]


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


def _obtener_palabras_unicas_estrofa(estrofa: list[str]) -> list[str]:
    palabras = []
    vistas = set()

    for verso in estrofa:
        for palabra in obtener_palabras(verso):
            palabra_normalizada = _normalizar(palabra)
            if (
                len(palabra_normalizada) <= 2
                or palabra_normalizada in PALABRAS_EXCLUIDAS_RIMA
                or palabra_normalizada in vistas
            ):
                continue

            palabras.append(palabra)
            vistas.add(palabra_normalizada)

    return palabras


def _obtener_palabras_repetidas_estrofa(estrofa: list[str]) -> set[str]:
    conteos = {}

    for verso in estrofa:
        for palabra in obtener_palabras(verso):
            palabra_normalizada = _normalizar(palabra)
            if (
                len(palabra_normalizada) <= 2
                or palabra_normalizada in PALABRAS_EXCLUIDAS_RIMA
            ):
                continue

            conteos[palabra_normalizada] = conteos.get(palabra_normalizada, 0) + 1

    return {palabra for palabra, conteo in conteos.items() if conteo >= 3}


def _agrupar_palabras_por_fragmento(
    palabras: list[str],
    tipo: str,
) -> dict[str, list[str]]:
    grupos: dict[str, list[str]] = {}

    for palabra in palabras:
        clave = _normalizar(obtener_fragmento_rimante(palabra, tipo))
        if clave:
            grupos.setdefault(clave, []).append(palabra)

    return grupos


def _grupo_relevante_para_resumen(
    palabras_grupo: list[str],
    palabras_finales: set[str],
    palabras_repetidas: set[str],
) -> bool:
    palabras_normalizadas = {_normalizar(palabra) for palabra in palabras_grupo}
    if len(palabras_grupo) >= 3:
        return True

    if palabras_normalizadas & palabras_repetidas:
        return True

    return len(palabras_normalizadas & palabras_finales) >= 2


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


def _tienen_clave_asonante_fuerte(palabra1: str, palabra2: str) -> bool:
    clave1 = obtener_clave_asonante(palabra1)
    clave2 = obtener_clave_asonante(palabra2)
    return len(clave1) >= 2 and clave1 == clave2


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


def _obtener_nucleos_vocalicos_asonantes(palabra: str) -> list[tuple[int, int]]:
    nucleos = []
    indice = 0

    while indice < len(palabra):
        if not _es_vocal_sonora(palabra, indice):
            indice += 1
            continue

        inicio = indice
        fin = indice
        indice += 1

        while indice < len(palabra) and _es_vocal_sonora(palabra, indice):
            if _forman_diptongo_asonante(palabra[fin], palabra[indice]):
                fin = indice
                indice += 1
                continue
            break

        nucleos.append((inicio, fin))

    return nucleos


def _obtener_indice_nucleo_por_posicion(
    nucleos: list[tuple[int, int]],
    posicion: int,
) -> int:
    for indice, (inicio, fin) in enumerate(nucleos):
        if inicio <= posicion <= fin:
            return indice
        if posicion < inicio:
            return indice

    return len(nucleos) - 1


def _vocal_representativa_asonante(palabra: str, nucleo: tuple[int, int]) -> str:
    inicio, fin = nucleo
    vocales = palabra[inicio : fin + 1]
    for vocal in vocales:
        if vocal in VOCALES_TILDADAS:
            return _normalizar(vocal)

    fuertes = [vocal for vocal in vocales if vocal in VOCALES_FUERTES]
    if fuertes:
        return _normalizar(fuertes[-1])

    return _normalizar(vocales[-1])


def _forman_diptongo_asonante(primera: str, segunda: str) -> bool:
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


def _es_vocal_sonora(palabra: str, indice: int) -> bool:
    letra = palabra[indice]
    if letra not in VOCALES:
        return False

    anterior = palabra[indice - 1].lower() if indice > 0 else ""
    siguiente = palabra[indice + 1].lower() if indice + 1 < len(palabra) else ""
    return not (letra.lower() == "u" and anterior == "q" and siguiente in {"e", "i"})


def _es_esdrujula(palabra: str) -> bool:
    silabas = separar_silabas_palabra(palabra)
    if len(silabas) < 3:
        return False

    indice_silaba_tonica = _obtener_indice_silaba_tonica_con_o_sin_tilde(
        palabra,
        silabas,
    )
    return indice_silaba_tonica <= len(silabas) - 3


def _obtener_indice_silaba_tonica_con_o_sin_tilde(
    palabra: str,
    silabas: list[str],
) -> int:
    indice_letra = 0
    for indice_silaba, silaba in enumerate(silabas):
        fin_silaba = indice_letra + len(silaba)
        if any(
            letra in VOCALES_TILDADAS
            for letra in palabra[indice_letra:fin_silaba]
        ):
            return indice_silaba
        indice_letra = fin_silaba

    return _obtener_indice_silaba_tonica_sin_tilde(palabra, silabas)

def agrupar_rimas_simples_por_estrofa(estrofas: list[list[str]]) -> list[dict]:
    grupos_por_estrofa = []

    for indice_estrofa, estrofa in enumerate(estrofas, start=1):
        grupos_por_clave = {}

        for verso in estrofa:
            for palabra in obtener_palabras(verso):
                normalizada = _normalizar(palabra)

                if len(normalizada) <= 2:
                    continue

                if normalizada in PALABRAS_EXCLUIDAS_RIMA:
                    continue

                clave = obtener_clave_asonante(palabra)

                if not clave:
                    continue

                grupos_por_clave.setdefault(clave, [])

                if palabra not in grupos_por_clave[clave]:
                    grupos_por_clave[clave].append(palabra)

        grupos = []
        indice_grupo = 0

        for clave, palabras in grupos_por_clave.items():
            if len(palabras) < 2:
                continue

            grupos.append(
                {
                    "grupo": _letra_de_esquema(indice_grupo),
                    "palabras": palabras,
                }
            )
            indice_grupo += 1

        grupos_por_estrofa.append(
            {
                "estrofa": indice_estrofa,
                "grupos": grupos,
            }
        )

    return grupos_por_estrofa

