"""Reflex entry point for the Rimador application."""

from html import escape

import reflex as rx

from core.metrica import analizar_metrica_verso, resumir_metrica_texto
from core.rima import (
    clasificar_rima,
    detectar_rimas_en_texto,
    obtener_esquema_rima,
    obtener_fragmento_rimante,
    obtener_ultima_palabra,
)
from core.ritmo import obtener_posiciones_acentuadas_verso
from core.utils.texto import obtener_palabras, obtener_versos


EDITOR_FONT_SIZE = "14px"
EDITOR_LINE_HEIGHT = "22px"
EDITOR_PADDING = "16px"
INLINE_RHYME_HEIGHT = "18px"
ANALYSIS_GRID_COLUMNS = "minmax(0, 1fr) 42px minmax(0, 1fr) 42px"
BORDER_RADIUS = "12px"
BORDER_COLOR = "#D9DEE8"
BORDER = f"1px solid {BORDER_COLOR}"
PANEL_BACKGROUND = "#FFFFFF"
SOFT_BACKGROUND = "#F8FAFC"
PANEL_PADDING = "16px"
TEXT_PRIMARY = "#1F2328"
TEXT_SECONDARY = "#4B5563"
TEXT_ON_ACCENT = "#FFFFFF"
TEXT_PRIMARY_DARK = "#F8FAFC"
TEXT_SECONDARY_DARK = "#CBD5E1"
CARD_BACKGROUND = "#FFFFFF"
CARD_BACKGROUND_DARK = "#1E293B"
CARD_BORDER = "#D9DEE8"
CARD_BORDER_DARK = "#334155"
ACCENT_BACKGROUND = "#0F8BEF"
ACCENT_BACKGROUND_SOFT = "#E8F3FE"
DONATION_URL = "https://link.mercadopago.cl/biteroom"
DONATION_OPTIONS = [
    ("☕ Aporte libre", "https://link.mercadopago.cl/biteroom"),
    ("CLP $1.000", "https://mpago.la/29SRa9z"),
    ("CLP $5.000", "https://mpago.la/1JeQaMT"),
    ("CLP $10.000", "https://mpago.la/1osswVX"),
]
LOGO_SRC = "/logo/logo.png"
FAVICON_SRC = "/favicon.png"

CONCEPTOS_APRENDER = [
    {
        "id": "silabas-gramaticales",
        "titulo": "Sílabas gramaticales",
        "categoria": "Métrica",
        "definicion": "Cantidad de sílabas de una palabra o verso según la división silábica ordinaria de la lengua.",
        "ejemplo": "En “casa blanca”, la división gramatical es ca-sa blan-ca: cuatro sílabas gramaticales.",
        "uso_en_rimador": "Rimador las usa como punto de partida antes de aplicar fenómenos métricos propios del verso.",
    },
    {
        "id": "silabas-metricas",
        "titulo": "Sílabas métricas",
        "categoria": "Métrica",
        "definicion": "Cantidad de sílabas consideradas en el verso poético, aplicando fenómenos como la sinalefa y el ajuste por palabra final aguda, llana o esdrújula.",
        "ejemplo": "“Mi alma” tiene tres sílabas gramaticales, pero puede contarse como dos sílabas métricas por sinalefa.",
        "uso_en_rimador": "Rimador muestra este conteo junto a cada verso y lo usa para clasificar el tipo de verso.",
    },
    {
        "id": "sinalefa",
        "titulo": "Sinalefa",
        "categoria": "Métrica",
        "definicion": "Unión métrica entre la vocal final de una palabra y la vocal inicial de la siguiente. Reduce el conteo métrico del verso.",
        "ejemplo": "En “la estrella”, la vocal final de “la” se une con la vocal inicial de “estrella”.",
        "uso_en_rimador": "Rimador detecta sinalefas básicas y las resta del conteo métrico del verso.",
    },
    {
        "id": "rima-consonante",
        "titulo": "Rima consonante",
        "categoria": "Rima",
        "definicion": "Coincidencia de vocales y consonantes desde la vocal tónica final de dos o más versos o palabras.",
        "ejemplo": "“Rima”, “tarima” y “cima” comparten la terminación “ima”.",
        "uso_en_rimador": "Rimador la marca con un resaltado más fuerte para rimas finales e internas.",
    },
    {
        "id": "rima-asonante",
        "titulo": "Rima asonante",
        "categoria": "Rima",
        "definicion": "Coincidencia solo de las vocales desde la vocal tónica final de dos o más versos o palabras.",
        "ejemplo": "“Casa” y “rama” comparten las vocales “a-a”, aunque sus consonantes cambian.",
        "uso_en_rimador": "Rimador la muestra con subrayado para distinguirla de la rima consonante.",
    },
    {
        "id": "verso",
        "titulo": "Verso",
        "categoria": "Estructura",
        "definicion": "Cada línea intencional de un poema o composición lírica.",
        "ejemplo": "En una canción escrita línea por línea, cada línea puede funcionar como verso.",
        "uso_en_rimador": "Rimador analiza cada verso por separado para medir sílabas, ritmo y rima.",
    },
    {
        "id": "estrofa",
        "titulo": "Estrofa",
        "categoria": "Estructura",
        "definicion": "Conjunto de versos agrupados dentro de una composición.",
        "ejemplo": "Una estrofa puede reunir cuatro versos con un patrón de rima como A B A B.",
        "uso_en_rimador": "Rimador trabaja sobre el texto completo y permite observar patrones entre versos agrupados.",
    },
]


class State(rx.State):
    """Application state shared by the Reflex app."""

    seccion_actual: str = "analizador"
    texto: str = ""
    resultados: list[dict] = []
    lineas_vista: list[dict] = []
    esquema_rima: list[str] = []
    resumen_cantidad_versos: int = 0
    resumen_tipo_predominante: str = "Sin versos"
    resumen_regularidad: str = "regular"
    resumen_esquema_rima: str = "Sin esquema"
    busqueda_aprender: str = ""
    concepto_seleccionado: str = "silabas-gramaticales"
    panel_donacion_abierto: bool = False

    @rx.var
    def conceptos_filtrados(self) -> list[dict]:
        """Return learning concepts matching the current search."""
        busqueda = self.busqueda_aprender.strip().lower()
        if not busqueda:
            return CONCEPTOS_APRENDER

        return [
            concepto
            for concepto in CONCEPTOS_APRENDER
            if busqueda in concepto["titulo"].lower()
            or busqueda in concepto["categoria"].lower()
            or busqueda in concepto["definicion"].lower()
        ]

    @rx.var
    def hay_conceptos_filtrados(self) -> bool:
        """Return whether the learning search has visible results."""
        return bool(self.conceptos_filtrados)

    @rx.var
    def concepto_actual(self) -> dict:
        """Return the selected learning concept."""
        for concepto in CONCEPTOS_APRENDER:
            if concepto["id"] == self.concepto_seleccionado:
                return concepto

        return CONCEPTOS_APRENDER[0]

    def mostrar_analizador(self):
        """Show the analyzer section."""
        self.seccion_actual = "analizador"

    def mostrar_aprender(self):
        """Show the learning section."""
        self.seccion_actual = "aprender"

    def mostrar_acerca_de(self):
        """Show the about section."""
        self.seccion_actual = "acerca_de"

    def buscar_conceptos(self, busqueda: str):
        """Update the learning concept search."""
        self.busqueda_aprender = busqueda

    def seleccionar_concepto(self, concepto_id: str):
        """Select one learning concept."""
        self.concepto_seleccionado = concepto_id

    def alternar_panel_donacion(self):
        """Toggle the donation support panel."""
        self.panel_donacion_abierto = not self.panel_donacion_abierto

    def abrir_panel_donacion(self):
        """Open the donation support panel."""
        self.panel_donacion_abierto = True

    def cerrar_panel_donacion(self):
        """Close the donation support panel."""
        self.panel_donacion_abierto = False

    def analizar(self, texto: str):
        """Analyze the entered text verse by verse."""
        self.texto = texto
        versos = obtener_versos(texto)
        self.esquema_rima = obtener_esquema_rima(versos)
        resumen_metrica = resumir_metrica_texto(versos)
        self.resumen_cantidad_versos = resumen_metrica["cantidad_versos"]
        self.resumen_tipo_predominante = (
            resumen_metrica["tipo_predominante"] or "Sin versos"
        )
        self.resumen_regularidad = (
            "regular" if resumen_metrica["es_regular"] else "irregular"
        )
        self.resumen_esquema_rima = " ".join(self.esquema_rima) or "Sin esquema"
        self.resultados = []
        rimas_en_texto = detectar_rimas_en_texto(versos)
        # Final rhyme letters and internal rhyme networks are styled separately.
        # A/B/C colors belong only to final words; internal groups use rhyme keys.
        rimas_internas_por_verso = _asignar_grupos_rimas_internas(
            rimas_en_texto,
            versos,
        )
        palabras_finales = [obtener_ultima_palabra(verso) for verso in versos]
        tipos_rima = _obtener_tipos_rima_por_verso(
            palabras_finales,
            self.esquema_rima,
        )

        for indice, verso in enumerate(versos):
            analisis = analizar_metrica_verso(verso)
            posiciones_acentuadas = obtener_posiciones_acentuadas_verso(verso)
            letra_rima = self.esquema_rima[indice] if indice < len(self.esquema_rima) else ""
            ultima_palabra = palabras_finales[indice]
            tipo_rima = tipos_rima[indice]
            fragmento_rimante = obtener_fragmento_rimante(
                ultima_palabra,
                tipo_rima,
            )
            vista_rima = _preparar_vista_rima(
                verso,
                ultima_palabra,
                fragmento_rimante,
                letra_rima,
            )
            rimas_internas_verso = rimas_internas_por_verso.get(indice, {})
            rimas_internas = _preparar_rimas_globales_verso(rimas_internas_verso)
            html_vista_rima = _preparar_html_vista_rima(
                verso,
                {"letra": letra_rima, "tipo": tipo_rima},
                rimas_internas_verso,
                ultima_palabra,
            )

            self.resultados.append(
                {
                    "texto": analisis["verso"],
                    "silabas_gramaticales": analisis["silabas_gramaticales"],
                    "silabas_metricas": analisis["silabas_metricas"],
                    "tipo_verso": analisis["tipo_verso"],
                    "sinalefas": _formatear_sinalefas(analisis["sinalefas"]),
                    "ajuste_final": _formatear_ajuste_final(
                        analisis["ajuste_final"],
                        analisis["tipo_palabra_final"],
                    ),
                    "posiciones_acentuadas": posiciones_acentuadas,
                    "posiciones_acentuadas_texto": str(posiciones_acentuadas),
                    "ultima_palabra": ultima_palabra,
                    "fragmento_rimante": fragmento_rimante,
                    "tipo_rima": tipo_rima,
                    "letra_rima": letra_rima,
                    "texto_antes_ultima_palabra": vista_rima[
                        "texto_antes_ultima_palabra"
                    ],
                    "ultima_palabra_prefijo": vista_rima["ultima_palabra_prefijo"],
                    "fragmento_resaltado": vista_rima["fragmento_resaltado"],
                    "color_rima": vista_rima["color_rima"],
                    "resaltar_rima": vista_rima["resaltar_rima"],
                    "rimas_internas": rimas_internas,
                    "tiene_rimas_internas": bool(rimas_internas),
                    "rimas_internas_texto": _formatear_rimas_internas(
                        rimas_internas
                    ),
                    "html_vista_rima": html_vista_rima,
                }
            )

        self.lineas_vista = _preparar_lineas_vista(texto, self.resultados)


def _formatear_sinalefas(sinalefas: list[dict]) -> str:
    if not sinalefas:
        return "Sin sinalefas"

    return ", ".join(
        f"{sinalefa['anterior']} + {sinalefa['siguiente']}"
        for sinalefa in sinalefas
    )


def _formatear_ajuste_final(ajuste_final: int, tipo_palabra_final: str) -> str:
    explicaciones = {
        "aguda": "+1 por palabra aguda",
        "llana": "0 por palabra llana",
        "esdrujula": "-1 por palabra esdrújula",
    }

    if ajuste_final == 0 and tipo_palabra_final != "llana":
        return "0 sin ajuste final"

    return explicaciones.get(tipo_palabra_final, str(ajuste_final))


def _formatear_rimas_internas(rimas_internas: list[dict]) -> str:
    if not rimas_internas:
        return "Sin rimas internas"

    return "\n".join(
        f"{rima['palabra']}: {rima['tipo']} ({rima['grupo_interno']})"
        for rima in rimas_internas
    )


def _preparar_rimas_globales_verso(rimas_en_verso: dict[int, dict]) -> list[dict]:
    return [
        rima
        for _, rima in sorted(rimas_en_verso.items())
    ]


def _asignar_grupos_rimas_internas(
    rimas_en_texto: dict[int, dict[int, dict]],
    versos: list[str],
) -> dict[int, dict[int, dict]]:
    """Keep global internal rhyme groups separate from final scheme letters."""
    rimas_internas = {}

    for indice_verso, rimas_verso in rimas_en_texto.items():
        indice_ultima_palabra = len(obtener_palabras(versos[indice_verso])) - 1

        for indice_palabra, rima in rimas_verso.items():
            if indice_palabra == indice_ultima_palabra:
                continue

            rimas_internas.setdefault(indice_verso, {})[indice_palabra] = {
                **rima
            }

    return rimas_internas


def _obtener_tipos_rima_por_verso(
    palabras_finales: list[str],
    esquema_rima: list[str],
) -> list[str]:
    tipos = []

    for indice, (palabra_actual, letra_actual) in enumerate(
        zip(palabras_finales, esquema_rima)
    ):
        tipo = "sin_rima"

        for otro_indice, (otra_palabra, otra_letra) in enumerate(
            zip(palabras_finales, esquema_rima)
        ):
            if indice == otro_indice or letra_actual != otra_letra:
                continue

            tipo = clasificar_rima(palabra_actual, otra_palabra)
            if tipo != "sin_rima":
                break

        tipos.append(tipo)

    return tipos


def _preparar_lineas_vista(texto: str, resultados: list[dict]) -> list[dict]:
    lineas_vista = []
    indice_resultado = 0

    for linea in texto.splitlines():
        if not linea.strip():
            lineas_vista.append(
                {
                    "html_vista_rima": "",
                    "silabas_gramaticales": None,
                    "silabas_metricas": None,
                }
            )
            continue

        if indice_resultado < len(resultados):
            resultado = resultados[indice_resultado]
            lineas_vista.append(
                {
                    "html_vista_rima": resultado["html_vista_rima"],
                    "silabas_gramaticales": resultado["silabas_gramaticales"],
                    "silabas_metricas": resultado["silabas_metricas"],
                }
            )
            indice_resultado += 1

    return lineas_vista


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


def _preparar_vista_rima(
    verso: str,
    ultima_palabra: str,
    fragmento_rimante: str,
    letra_rima: str,
) -> dict:
    if not ultima_palabra:
        return {
            "texto_antes_ultima_palabra": verso,
            "ultima_palabra_prefijo": "",
            "fragmento_resaltado": "",
            "color_rima": "",
            "resaltar_rima": False,
        }

    inicio_ultima_palabra = verso.rfind(ultima_palabra)
    texto_antes = (
        verso[:inicio_ultima_palabra].rstrip()
        if inicio_ultima_palabra >= 0
        else ""
    )
    resaltar = bool(fragmento_rimante)

    if resaltar and ultima_palabra.endswith(fragmento_rimante):
        prefijo = ultima_palabra[: -len(fragmento_rimante)]
        resaltado = fragmento_rimante
    elif resaltar:
        prefijo = ""
        resaltado = ultima_palabra
    else:
        prefijo = ultima_palabra
        resaltado = ""

    return {
        "texto_antes_ultima_palabra": texto_antes,
        "ultima_palabra_prefijo": prefijo,
        "fragmento_resaltado": resaltado,
        "color_rima": color_rima_final(letra_rima),
        "resaltar_rima": resaltar,
    }


def _preparar_html_vista_rima(
    verso: str,
    rima_final: dict,
    rimas_internas: dict[int, dict],
    ultima_palabra: str,
) -> str:
    palabras = obtener_palabras(verso)
    if not palabras:
        return ""

    color_final = color_rima_final(rima_final["letra"])
    indice_ultima_palabra = len(palabras) - 1
    partes = []

    for indice, palabra in enumerate(palabras):
        rima_interna = rimas_internas.get(indice, {})
        if indice == indice_ultima_palabra and palabra == ultima_palabra:
            partes.append(
                _renderizar_palabra_rima_final(
                    palabra,
                    rima_final["tipo"],
                    color_final,
                )
            )
            continue

        partes.append(
            _renderizar_palabra_rima_interna(
                palabra,
                rima_interna.get("tipo", ""),
                color_rima_interna(rima_interna.get("grupo_interno", "")),
            )
        )

    return (
        '<span style="display:flex;flex-wrap:wrap;column-gap:0.5rem;'
        f"row-gap:0;align-items:center;line-height:{EDITOR_LINE_HEIGHT};"
        'margin:0;padding:0;">'
        + "".join(partes)
        + _renderizar_badge_rima(rima_final["letra"], color_final)
        + "</span>"
    )


def _renderizar_palabra_rima_final(
    palabra: str,
    tipo_rima: str,
    color: dict,
) -> str:
    """Render only the final word with the final rhyme scheme palette."""
    palabra_segura = escape(palabra)
    if tipo_rima in {"consonante", "sin_rima"}:
        return (
            f'<span style="background:{color["background"]};'
            f'border:1px solid {color["border"]};border-radius:6px;'
            f'color:{color["text"]};padding:0 4px;font-weight:700;'
            f"line-height:{EDITOR_LINE_HEIGHT};"
            f"height:{INLINE_RHYME_HEIGHT};display:inline-flex;"
            f'align-items:center;margin-top:0;margin-bottom:0;">'
            f"{palabra_segura}</span>"
        )

    if tipo_rima == "asonante":
        return (
            f'<span style="text-decoration:underline;'
            f'text-decoration-thickness:2px;text-decoration-color:{color["border"]};'
            f"text-underline-offset:0.18rem;font-weight:700;"
            f'color:{color["text"]};'
            f"line-height:{EDITOR_LINE_HEIGHT};height:{INLINE_RHYME_HEIGHT};"
            f"display:inline-flex;align-items:center;margin-top:0;"
            f'margin-bottom:0;padding-top:0;padding-bottom:0;">'
            f"{palabra_segura}</span>"
        )

    return (
        f"<span style=\"line-height:{EDITOR_LINE_HEIGHT};"
        f"height:{INLINE_RHYME_HEIGHT};display:inline-flex;"
        f"align-items:center;margin-top:0;margin-bottom:0;"
        f'padding-top:0;padding-bottom:0;">{palabra_segura}</span>'
    )


def _renderizar_palabra_rima_interna(
    palabra: str,
    tipo_rima: str,
    color: dict,
) -> str:
    """Render internal rhyme networks without final scheme badges or letters."""
    palabra_segura = escape(palabra)
    if tipo_rima == "consonante":
        return (
            f'<span style="border-bottom:3px solid {color["border"]};'
            f'color:{color["text"]};font-weight:700;'
            f"line-height:{EDITOR_LINE_HEIGHT};height:{INLINE_RHYME_HEIGHT};"
            f"display:inline-flex;align-items:center;margin-top:0;"
            f'margin-bottom:0;padding:0 1px;">{palabra_segura}</span>'
        )

    if tipo_rima == "asonante":
        return (
            f'<span style="text-decoration:underline;'
            f'text-decoration-style:dotted;'
            f'text-decoration-thickness:2px;text-decoration-color:{color["border"]};'
            f"text-underline-offset:0.22rem;font-weight:700;"
            f'color:{color["text"]};line-height:{EDITOR_LINE_HEIGHT};'
            f"height:{INLINE_RHYME_HEIGHT};display:inline-flex;"
            f"align-items:center;margin-top:0;margin-bottom:0;"
            f'padding-top:0;padding-bottom:0;">{palabra_segura}</span>'
        )

    return (
        f"<span style=\"line-height:{EDITOR_LINE_HEIGHT};"
        f"height:{INLINE_RHYME_HEIGHT};display:inline-flex;"
        f"align-items:center;margin-top:0;margin-bottom:0;"
        f'padding-top:0;padding-bottom:0;">{palabra_segura}</span>'
    )


def _renderizar_badge_rima(letra_rima: str, color: dict) -> str:
    if not letra_rima:
        return ""

    return (
        f'<span style="background:{color["background"]};color:{color["text"]};'
        f'border:1px solid {color["border"]};border-radius:999px;'
        f"padding:0 0.45rem;font-size:0.8rem;font-weight:700;"
        f"line-height:{EDITOR_LINE_HEIGHT};height:{INLINE_RHYME_HEIGHT};"
        f"display:inline-flex;align-items:center;margin-top:0;margin-bottom:0;"
        f'padding-top:0;padding-bottom:0;">'
        f"{escape(letra_rima)}</span>"
    )


def _fila_resultado(etiqueta: str, valor: rx.Var) -> rx.Component:
    return rx.hstack(
        rx.text(etiqueta, weight="bold"),
        rx.text(valor),
        spacing="2",
        align="start",
    )


def color_texto_principal():
    return rx.color_mode_cond(TEXT_PRIMARY, TEXT_PRIMARY_DARK)


def color_texto_secundario():
    return rx.color_mode_cond(TEXT_SECONDARY, TEXT_SECONDARY_DARK)


def fondo_panel():
    return rx.color_mode_cond(CARD_BACKGROUND, CARD_BACKGROUND_DARK)


def fondo_suave():
    return rx.color_mode_cond(SOFT_BACKGROUND, "#0F172A")


def borde_panel():
    return rx.color_mode_cond(
        f"1px solid {CARD_BORDER}",
        f"1px solid {CARD_BORDER_DARK}",
    )


def _resumen_item(etiqueta: str, valor: rx.Var) -> rx.Component:
    return rx.vstack(
        rx.text(etiqueta, size="2", color=color_texto_secundario()),
        rx.text(valor, weight="bold", color=color_texto_principal()),
        spacing="1",
        align="start",
    )


def panel_resumen() -> rx.Component:
    """Render the text-level metric and rhyme summary."""
    return rx.card(
        rx.vstack(
            rx.heading("Resumen", size="4"),
            rx.grid(
                _resumen_item("Versos", State.resumen_cantidad_versos),
                _resumen_item(
                    "Métrica predominante",
                    State.resumen_tipo_predominante,
                ),
                _resumen_item("Regularidad", State.resumen_regularidad),
                _resumen_item("Esquema de rima", State.resumen_esquema_rima),
                columns="repeat(auto-fit, minmax(160px, 1fr))",
                spacing="4",
                width="100%",
            ),
            spacing="3",
            align="stretch",
        ),
        width="100%",
        padding=PANEL_PADDING,
        border=borde_panel(),
        border_radius=BORDER_RADIUS,
        background=fondo_panel(),
        color=color_texto_principal(),
    )


def boton_navegacion(etiqueta: str, seccion: str, accion) -> rx.Component:
    return rx.button(
        etiqueta,
        on_click=accion,
        variant=rx.cond(State.seccion_actual == seccion, "solid", "soft"),
        size="2",
        border_radius="10px",
        color=rx.cond(
            State.seccion_actual == seccion,
            TEXT_ON_ACCENT,
            color_texto_principal(),
        ),
    )


def menu_superior() -> rx.Component:
    return rx.hstack(
        boton_navegacion("Analizador", "analizador", State.mostrar_analizador),
        boton_navegacion("Aprender", "aprender", State.mostrar_aprender),
        boton_navegacion("Acerca de", "acerca_de", State.mostrar_acerca_de),
        spacing="3",
        align="center",
        wrap="wrap",
    )


def vista_rima_verso(resultado: dict) -> rx.Component:
    """Render one verse with its rhyme fragment highlighted."""
    return rx.box(
        rx.html(resultado["html_vista_rima"]),
        display="flex",
        align_items="center",
        height=EDITOR_LINE_HEIGHT,
        margin="0",
        padding="0",
        line_height=EDITOR_LINE_HEIGHT,
        min_height=EDITOR_LINE_HEIGHT,
        width="100%",
    )


def contador_silabas(valor: int | None, tooltip: str) -> rx.Component:
    """Render one line-aligned syllable counter."""
    contenido = rx.box(
        rx.text(
            valor,
            size="1",
            weight="bold",
            line_height=EDITOR_LINE_HEIGHT,
        ),
        display="flex",
        align_items="center",
        justify_content="center",
        width="26px",
        height="18px",
        border=borde_panel(),
        border_radius="4px",
        background=fondo_panel(),
        color=color_texto_principal(),
    )

    return rx.box(
        rx.cond(
            valor != None,
            rx.tooltip(contenido, content=tooltip),
            rx.box(),
        ),
        display="flex",
        align_items="center",
        justify_content="center",
        height=EDITOR_LINE_HEIGHT,
        min_height=EDITOR_LINE_HEIGHT,
        margin="0",
        padding="0",
        line_height=EDITOR_LINE_HEIGHT,
        width="100%",
    )


def contador_silabas_gramaticales(linea: dict) -> rx.Component:
    return contador_silabas(
        linea["silabas_gramaticales"],
        "Cantidad de sílabas gramaticales",
    )


def contador_silabas_metricas(linea: dict) -> rx.Component:
    return contador_silabas(
        linea["silabas_metricas"],
        "Cantidad de sílabas métricas",
    )


def rimas_internas_resultado(resultado: dict) -> rx.Component:
    """Render internal rhymes for one verse."""
    return rx.vstack(
        rx.text("Rimas internas:", weight="bold"),
        rx.cond(
            resultado["tiene_rimas_internas"],
            rx.text(resultado["rimas_internas_texto"], white_space="pre-line"),
            rx.text("Sin rimas internas"),
        ),
        spacing="1",
        align="start",
    )


def tarjeta_verso(resultado: dict) -> rx.Component:
    """Render one verse analysis card."""
    return rx.card(
        rx.vstack(
            rx.text(resultado["texto"], weight="bold", size="4"),
            _fila_resultado("Sílabas gramaticales:", resultado["silabas_gramaticales"]),
            rx.hstack(
                rx.text("Sílabas métricas:", weight="bold"),
                rx.text(resultado["silabas_metricas"]),
                rx.badge(resultado["tipo_verso"]),
                spacing="2",
                align="center",
            ),
            _fila_resultado("Sinalefas detectadas:", resultado["sinalefas"]),
            _fila_resultado("Ajuste final:", resultado["ajuste_final"]),
            _fila_resultado(
                "Posiciones acentuadas:",
                resultado["posiciones_acentuadas_texto"],
            ),
            _fila_resultado("Última palabra:", resultado["ultima_palabra"]),
            rx.hstack(
                rx.text("Fragmento rimante:", weight="bold"),
                rx.badge(resultado["fragmento_rimante"]),
                spacing="2",
                align="start",
            ),
            _fila_resultado("Tipo:", resultado["tipo_rima"]),
            _fila_resultado("Esquema de rima:", resultado["letra_rima"]),
            rimas_internas_resultado(resultado),
            spacing="2",
            align="start",
        ),
        width="100%",
        padding=PANEL_PADDING,
        border=borde_panel(),
        border_radius=BORDER_RADIUS,
        background=fondo_panel(),
        color=color_texto_principal(),
    )


def seccion_analizador() -> rx.Component:
    return rx.vstack(
        panel_resumen(),
        rx.vstack(
            rx.grid(
                rx.heading("Escribe tu texto", size="5"),
                rx.box(),
                rx.heading("Vista analizada", size="5"),
                rx.box(),
                columns=ANALYSIS_GRID_COLUMNS,
                spacing="3",
                width="100%",
            ),
            rx.grid(
                rx.text_area(
                    placeholder="Escribe un poema o varios versos...",
                    value=State.texto,
                    on_change=State.analizar,
                    width="100%",
                    font_family="monospace",
                    font_size=EDITOR_FONT_SIZE,
                    line_height=EDITOR_LINE_HEIGHT,
                    padding=EDITOR_PADDING,
                    height="500px",
                    border=borde_panel(),
                    border_radius=BORDER_RADIUS,
                    background=fondo_panel(),
                    color=color_texto_principal(),
                ),
                rx.box(
                    rx.vstack(
                        rx.foreach(
                            State.lineas_vista,
                            contador_silabas_gramaticales,
                        ),
                        spacing="0",
                        align="stretch",
                        width="100%",
                    ),
                    width="100%",
                    height="500px",
                    padding_y=EDITOR_PADDING,
                    overflow_y="auto",
                ),
                rx.box(
                    rx.vstack(
                        rx.foreach(State.lineas_vista, vista_rima_verso),
                        spacing="0",
                        align="start",
                        width="100%",
                    ),
                    width="100%",
                    font_family="monospace",
                    font_size=EDITOR_FONT_SIZE,
                    line_height=EDITOR_LINE_HEIGHT,
                    white_space="pre-wrap",
                    height="500px",
                    padding=EDITOR_PADDING,
                    border=borde_panel(),
                    border_radius=BORDER_RADIUS,
                    background=fondo_suave(),
                    color=color_texto_principal(),
                    overflow_y="auto",
                ),
                rx.box(
                    rx.vstack(
                        rx.foreach(State.lineas_vista, contador_silabas_metricas),
                        spacing="0",
                        align="stretch",
                        width="100%",
                    ),
                    width="100%",
                    height="500px",
                    padding_y=EDITOR_PADDING,
                    overflow_y="auto",
                ),
                columns=ANALYSIS_GRID_COLUMNS,
                spacing="3",
                width="100%",
            ),
            spacing="3",
            align="stretch",
            width="100%",
        ),
        rx.vstack(
            rx.foreach(State.resultados, tarjeta_verso),
            spacing="4",
            width="100%",
        ),
        spacing="5",
        align="stretch",
        width="100%",
    )


def item_concepto_aprender(concepto: dict) -> rx.Component:
    seleccionado = State.concepto_seleccionado == concepto["id"]
    return rx.button(
        rx.vstack(
            rx.text(
                concepto["titulo"],
                weight="bold",
                color=rx.cond(seleccionado, TEXT_ON_ACCENT, color_texto_principal()),
            ),
            rx.text(
                concepto["categoria"],
                size="2",
                color=rx.cond(seleccionado, "rgba(255,255,255,0.82)", color_texto_secundario()),
            ),
            spacing="1",
            align="start",
            width="100%",
        ),
        on_click=State.seleccionar_concepto(concepto["id"]),
        variant="soft",
        width="100%",
        justify_content="start",
        height="auto",
        padding=PANEL_PADDING,
        border=rx.cond(seleccionado, f"1px solid {ACCENT_BACKGROUND}", borde_panel()),
        border_radius=BORDER_RADIUS,
        background=rx.cond(seleccionado, ACCENT_BACKGROUND, fondo_panel()),
        color=rx.cond(seleccionado, TEXT_ON_ACCENT, color_texto_principal()),
    )


def lista_conceptos_aprender() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.cond(
                State.hay_conceptos_filtrados,
                rx.vstack(
                    rx.foreach(State.conceptos_filtrados, item_concepto_aprender),
                    spacing="2",
                    width="100%",
                ),
                rx.text("No se encontraron conceptos.", color=color_texto_secundario()),
            ),
            spacing="3",
            align="stretch",
        ),
        width="100%",
        padding=PANEL_PADDING,
        border=borde_panel(),
        border_radius=BORDER_RADIUS,
        background=fondo_panel(),
        color=color_texto_principal(),
    )


def detalle_concepto_aprender() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.heading(State.concepto_actual["titulo"], size="6"),
                rx.badge(State.concepto_actual["categoria"]),
                spacing="3",
                align="center",
                wrap="wrap",
            ),
            rx.vstack(
                rx.text("Definición", weight="bold"),
                rx.text(State.concepto_actual["definicion"], color=color_texto_secundario()),
                spacing="1",
                align="start",
            ),
            rx.vstack(
                rx.text("Ejemplo", weight="bold"),
                rx.text(State.concepto_actual["ejemplo"], color=color_texto_secundario()),
                spacing="1",
                align="start",
            ),
            rx.vstack(
                rx.text("Cómo lo usa Rimador", weight="bold"),
                rx.text(State.concepto_actual["uso_en_rimador"], color=color_texto_secundario()),
                spacing="1",
                align="start",
            ),
            spacing="4",
            align="stretch",
        ),
        width="100%",
        padding=PANEL_PADDING,
        border=borde_panel(),
        border_radius=BORDER_RADIUS,
        background=fondo_panel(),
        color=color_texto_principal(),
    )


def seccion_aprender() -> rx.Component:
    return rx.vstack(
        rx.heading("Aprender", size="7"),
        rx.input(
            placeholder="Buscar conceptos...",
            value=State.busqueda_aprender,
            on_change=State.buscar_conceptos,
            width="100%",
            border=borde_panel(),
            border_radius=BORDER_RADIUS,
            background=fondo_panel(),
            color=color_texto_principal(),
        ),
        rx.grid(
            lista_conceptos_aprender(),
            detalle_concepto_aprender(),
            columns="minmax(220px, 0.8fr) minmax(0, 1.4fr)",
            spacing="4",
            width="100%",
        ),
        spacing="4",
        align="stretch",
        width="100%",
    )


def seccion_acerca_de() -> rx.Component:
    return rx.vstack(
        rx.heading("Acerca de", size="7"),
        rx.card(
            rx.vstack(
                rx.text(
                    "Rimador es una herramienta gratuita y experimental para analizar escritura creativa en español. Su objetivo es ayudar a poetas, músicos, raperos, compositores y escritores a comprender mejor la métrica, la rima y el ritmo de sus textos.",
                    color=color_texto_secundario(),
                ),
                rx.text(
                    "El proyecto busca unir tecnología, lingüística y creación artística en una herramienta accesible. Rimador no pretende reemplazar la intuición creativa ni dictar cómo debe escribirse un poema o una canción, sino ofrecer una lectura técnica que ayude a descubrir patrones, posibilidades y detalles del texto.",
                    color=color_texto_secundario(),
                ),
                rx.text(
                    "Esta versión beta puede cometer errores, especialmente en casos interpretativos como hiato poético, sinéresis, diéresis, licencias expresivas o rimas complejas. Por eso, los resultados deben entenderse como una ayuda orientativa, no como una sentencia absoluta.",
                    color=color_texto_secundario(),
                ),
                rx.text(
                    "Rimador es gratuito. Si la herramienta te resulta útil y quieres apoyar su desarrollo, puedes realizar una donación voluntaria. Ese apoyo ayuda a mantener el proyecto, mejorar los análisis y agregar nuevo contenido educativo.",
                    color=color_texto_secundario(),
                ),
                rx.button(
                    "Apoyar con una donación",
                    background=ACCENT_BACKGROUND,
                    color=TEXT_ON_ACCENT,
                    border_radius="10px",
                    on_click=State.abrir_panel_donacion,
                ),
                spacing="3",
                align="start",
            ),
            width="100%",
            padding=PANEL_PADDING,
            border=borde_panel(),
            border_radius=BORDER_RADIUS,
            background=fondo_panel(),
            color=color_texto_principal(),
        ),
        spacing="4",
        align="stretch",
        width="100%",
    )


def contenido_actual() -> rx.Component:
    return rx.cond(
        State.seccion_actual == "aprender",
        seccion_aprender(),
        rx.cond(
            State.seccion_actual == "acerca_de",
            seccion_acerca_de(),
            seccion_analizador(),
        ),
    )


def opcion_donacion(etiqueta: str, url: str) -> rx.Component:
    return rx.link(
        rx.button(
            etiqueta,
            variant="soft",
            width="100%",
            justify_content="start",
            border_radius="10px",
            color=color_texto_principal(),
        ),
        href=url,
        is_external=True,
        width="100%",
    )


def panel_donacion() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.heading("Apoya el proyecto", size="4", color=color_texto_principal()),
                rx.spacer(),
                rx.button(
                    "×",
                    on_click=State.cerrar_panel_donacion,
                    variant="soft",
                    border_radius="999px",
                    cursor="pointer",
                ),
                width="100%",
                align="center",
            ),
            rx.text(
                "Rimador es gratuito y se mantiene gracias al apoyo voluntario de personas que desean ayudar a su desarrollo.",
                color=color_texto_secundario(),
            ),
            rx.vstack(
                *[
                    opcion_donacion(etiqueta, url)
                    for etiqueta, url in DONATION_OPTIONS
                ],
                spacing="2",
                width="100%",
            ),
            spacing="3",
            align="stretch",
            width="100%",
        ),
        position="fixed",
        bottom="84px",
        right="24px",
        width="300px",
        padding=PANEL_PADDING,
        border=borde_panel(),
        border_radius=BORDER_RADIUS,
        background=fondo_panel(),
        box_shadow="0 18px 48px rgba(15, 23, 42, 0.24)",
        z_index="1000",
    )


def boton_donacion_flotante() -> rx.Component:
    return rx.vstack(
        rx.cond(State.panel_donacion_abierto, panel_donacion(), rx.box()),
        rx.button(
            "❤️ Apoyar Rimador",
            on_click=State.alternar_panel_donacion,
            background=ACCENT_BACKGROUND,
            color=TEXT_ON_ACCENT,
            border_radius="999px",
            padding_x="18px",
            box_shadow="0 10px 24px rgba(15, 139, 239, 0.28)",
            cursor="pointer",
            title="Apoya el desarrollo de Rimador",
        ),
        align="end",
        spacing="2",
    )


def encabezado_marca() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.image(
                src=LOGO_SRC,
                alt="Logo de Rimador",
                height="60px",
                width="90px",
                object_fit="cover",
                object_position="32% 50%",
                border_radius="10px",
            ),
            rx.heading("Rimador", size="9"),
            spacing="3",
            align="center",
        ),
        rx.text(
            "Analiza métrica, ritmo básico y rima verso a verso.",
            size="5",
        ),
        spacing="2",
        align="start",
    )


def index() -> rx.Component:
    """Render the initial page."""
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.box(
            boton_donacion_flotante(),
            position="fixed",
            bottom="24px",
            right="24px",
            z_index="1000",
            cursor="pointer",
        ),
        rx.vstack(
            rx.hstack(
                encabezado_marca(),
                menu_superior(),
                justify="between",
                align="center",
                width="100%",
                wrap="wrap",
                spacing="4",
            ),
            contenido_actual(),
            spacing="5",
            align="stretch",
            width="100%",
        ),
        max_width="1200px",
        padding_y="3rem",
    )


app = rx.App()
app.add_page(index, title="Rimador", image=FAVICON_SRC)
