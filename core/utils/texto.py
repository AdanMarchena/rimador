"""Utilities for preparing user-entered text for poetic analysis."""

SIGNOS_PUNTUACION_BASICOS = ".,;:!?\u00a1\u00bf\"'()[]{}"


def obtener_lineas(texto: str) -> list[str]:
    """Return user-entered logical lines, preserving the active final line."""
    if not texto:
        return []

    return texto.split("\n")


def obtener_versos(texto: str) -> list[str]:
    """Return real verses from user-entered text.

    A verse is defined by real newline characters (``\n``) entered by the
    user. This should not be confused with the editor's visual wrapping, which
    only changes how text is displayed on screen. Later, these verses will be
    analyzed for metric and rhythmic structure.
    """
    return [linea.strip() for linea in obtener_lineas(texto) if linea.strip()]


def obtener_estrofas(texto: str) -> list[list[str]]:
    """Return stanzas separated by one or more blank lines."""
    estrofas = []
    estrofa_actual = []

    for linea in obtener_lineas(texto):
        verso = linea.strip()
        if verso:
            estrofa_actual.append(verso)
            continue

        if estrofa_actual:
            estrofas.append(estrofa_actual)
            estrofa_actual = []

    if estrofa_actual:
        estrofas.append(estrofa_actual)

    return estrofas


def obtener_palabras(verso: str) -> list[str]:
    """Return clean words from a verse."""
    return [
        palabra_limpia
        for palabra in verso.split()
        if (palabra_limpia := palabra.strip(SIGNOS_PUNTUACION_BASICOS))
    ]
