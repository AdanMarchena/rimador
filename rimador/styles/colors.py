"""Rhyme color palettes."""


def color_rima_final(letra: str) -> dict:
    """Return colors reserved for final rhyme scheme letters."""
    paleta = [
        {"background": "#F7D6D9", "border": "#D9534F", "text": "#7A1F1F"},
        {"background": "#D6E8F7", "border": "#3A7BD5", "text": "#1B3A5A"},
        {"background": "#D8F2D6", "border": "#4CAF50", "text": "#1F5A22"},
        {"background": "#E8D6F7", "border": "#8E44AD", "text": "#4A235A"},
        {"background": "#F7E8D6", "border": "#E67E22", "text": "#6B3D0C"},
    ]
    colores_por_letra = {
        "A": paleta[0],
        "B": paleta[1],
        "C": paleta[2],
        "D": paleta[3],
        "E": paleta[4],
    }

    if not letra:
        return {"background": "#f3f4f6", "border": "#9ca3af", "text": "#374151"}

    return colores_por_letra.get(
        letra,
        paleta[sum(ord(caracter) for caracter in letra) % len(paleta)],
    )


def color_rima_interna(grupo: str) -> dict:
    """Return colors reserved for internal rhyme networks."""
    paleta = [
        {"border": "#0F766E", "text": "#115E59"},
        {"border": "#B45309", "text": "#78350F"},
        {"border": "#6D28D9", "text": "#4C1D95"},
        {"border": "#BE123C", "text": "#881337"},
        {"border": "#2563EB", "text": "#1E3A8A"},
    ]
    if not grupo:
        return {"border": "#6b7280", "text": "#374151"}

    return paleta[sum(ord(caracter) for caracter in grupo) % len(paleta)]
