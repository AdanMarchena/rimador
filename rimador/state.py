"""Application state and analysis preparation helpers."""

from html import escape

import reflex as rx

from core.exportacion.pdf import generar_pdf_analisis
from core.metrica import analizar_metrica_verso, resumir_metrica_texto
from core.rima import (
    clasificar_rima,
    detectar_rimas_en_texto,
    obtener_esquemas_rima_por_estrofa,
    obtener_fragmento_rimante,
    obtener_ultima_palabra,
)
from core.ritmo import obtener_posiciones_acentuadas_verso
from core.utils.texto import obtener_estrofas, obtener_palabras
from rimador.styles.colors import color_rima_final, color_rima_interna
from rimador.styles.theme import EDITOR_LINE_HEIGHT, INLINE_RHYME_HEIGHT
from rimador.version import APP_VERSION


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
    estrofas: list[list[str]] = []
    estrofas_analisis: list[dict] = []
    analisis_completo_items: list[dict] = []
    lineas_vista: list[dict] = []
    esquema_rima: list[str] = []
    esquemas_rima_por_estrofa: list[dict] = []
    resumen_cantidad_versos: int = 0
    resumen_cantidad_estrofas: int = 0
    resumen_tipo_predominante: str = "Sin versos"
    resumen_regularidad: str = "regular"
    resumen_esquemas_rima: list[dict] = []
    mostrar_advertencia_formato: bool = False
    texto_extenso: bool = False
    busqueda_aprender: str = ""
    concepto_seleccionado: str = "silabas-gramaticales"
    panel_donacion_abierto: bool = False
    version_vista: str = rx.LocalStorage("", name="rimador_version_vista")
    mostrar_modal_novedades: bool = False

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

    def verificar_novedades(self):
        """Show release notes once for each app version."""
        self.mostrar_modal_novedades = self.version_vista != APP_VERSION

    def cerrar_novedades(self):
        """Mark the current app version as seen."""
        self.version_vista = APP_VERSION
        self.mostrar_modal_novedades = False

    def mostrar_aprender(self):
        """Show the learning section."""
        self.seccion_actual = "aprender"

    def mostrar_acerca_de(self):
        """Show the about section."""
        self.seccion_actual = "acerca_de"

    def mostrar_analisis_completo(self):
        """Show the complete analysis section."""
        self.seccion_actual = "analisis_completo"

    def buscar_conceptos(self, busqueda: str):
        """Update the learning concept search."""
        self.busqueda_aprender = busqueda

    def seleccionar_concepto(self, concepto_id: str):
        """Select one learning concept."""
        self.concepto_seleccionado = concepto_id

    def ver_concepto_aprender(self, concepto_id: str):
        """Show the learning section focused on one concept."""
        if concepto_id:
            self.concepto_seleccionado = concepto_id
        self.seccion_actual = "aprender"

    def alternar_panel_donacion(self):
        """Toggle the donation support panel."""
        self.panel_donacion_abierto = not self.panel_donacion_abierto

    def abrir_panel_donacion(self):
        """Open the donation support panel."""
        self.panel_donacion_abierto = True

    def cerrar_panel_donacion(self):
        """Close the donation support panel."""
        self.panel_donacion_abierto = False

    def exportar_pdf(self):
        """Download the current complete analysis as a PDF."""
        pdf = generar_pdf_analisis(
            self.texto,
            self.resultados,
            {
                "versos_totales": self.resumen_cantidad_versos,
                "estrofas": self.resumen_cantidad_estrofas,
                "metrica_predominante": self.resumen_tipo_predominante,
                "regularidad": self.resumen_regularidad,
                "esquemas_rima": self.resumen_esquemas_rima,
            },
        )
        return rx.download(
            data=pdf,
            filename="analisis_rimador.pdf",
            mime_type="application/pdf",
        )

    def analizar(self, texto: str):
        """Analyze the entered text verse by verse."""
        self.texto = texto
        self.mostrar_advertencia_formato = len(texto) > 250 and texto.count("\n") < 2
        self.estrofas = obtener_estrofas(texto)
        versos = [
            verso
            for estrofa in self.estrofas
            for verso in estrofa
        ]
        self.esquemas_rima_por_estrofa = obtener_esquemas_rima_por_estrofa(
            self.estrofas
        )
        self.esquema_rima = [
            letra
            for esquema_estrofa in self.esquemas_rima_por_estrofa
            for letra in esquema_estrofa["esquema"]
        ]
        resumen_metrica = resumir_metrica_texto(versos)
        self.resumen_cantidad_versos = resumen_metrica["cantidad_versos"]
        self.resumen_cantidad_estrofas = len(self.estrofas)
        self.resumen_tipo_predominante = (
            resumen_metrica["tipo_predominante"] or "Sin versos"
        )
        self.resumen_regularidad = (
            "regular" if resumen_metrica["es_regular"] else "irregular"
        )
        self.resumen_esquemas_rima = _preparar_resumen_esquemas_rima(
            self.esquemas_rima_por_estrofa
        )
        self.texto_extenso = len(texto) > 700 or len(versos) > 12
        self.resultados = []
        self.estrofas_analisis = []
        self.analisis_completo_items = []
        rimas_en_texto = detectar_rimas_en_texto(versos)
        # Final rhyme letters and internal rhyme networks are styled separately.
        # A/B/C colors belong only to final words; internal groups use rhyme keys.
        rimas_internas_por_verso = _asignar_grupos_rimas_internas(
            rimas_en_texto,
            versos,
        )
        palabras_finales_por_estrofa = [
            [obtener_ultima_palabra(verso) for verso in estrofa]
            for estrofa in self.estrofas
        ]
        tipos_rima_por_estrofa = _obtener_tipos_rima_por_estrofa(
            palabras_finales_por_estrofa,
            self.esquemas_rima_por_estrofa,
        )
        palabras_finales = [
            palabra
            for palabras_estrofa in palabras_finales_por_estrofa
            for palabra in palabras_estrofa
        ]
        tipos_rima = [
            tipo
            for tipos_estrofa in tipos_rima_por_estrofa
            for tipo in tipos_estrofa
        ]

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
        self.estrofas_analisis = _preparar_estrofas_analisis(
            self.estrofas,
            self.esquemas_rima_por_estrofa,
            self.resultados,
        )
        self.analisis_completo_items = _preparar_analisis_completo_items(
            self.estrofas_analisis
        )


def _preparar_resumen_esquemas_rima(esquemas: list[dict]) -> list[dict]:
    if not esquemas:
        return [{"etiqueta": "Sin esquema", "esquema": ""}]

    return [
        {
            "etiqueta": f"Estrofa {esquema['estrofa']}",
            "esquema": esquema["esquema_texto"] or "Sin esquema",
        }
        for esquema in esquemas
    ]


def _preparar_estrofas_analisis(
    estrofas: list[list[str]],
    esquemas: list[dict],
    resultados: list[dict],
) -> list[dict]:
    estrofas_analisis = []
    indice_resultado = 0

    for indice, estrofa in enumerate(estrofas):
        cantidad_versos = len(estrofa)
        versos_analizados = resultados[indice_resultado:indice_resultado + cantidad_versos]
        esquema = esquemas[indice] if indice < len(esquemas) else {}
        estrofas_analisis.append(
            {
                "numero": indice + 1,
                "esquema_texto": esquema.get("esquema_texto", ""),
                "versos": versos_analizados,
            }
        )
        indice_resultado += cantidad_versos

    return estrofas_analisis


def _preparar_analisis_completo_items(estrofas_analisis: list[dict]) -> list[dict]:
    items = []

    for estrofa in estrofas_analisis:
        items.append(
            {
                "tipo_item": "estrofa",
                "numero": estrofa["numero"],
                "esquema_texto": estrofa["esquema_texto"],
            }
        )
        items.extend(
            {
                "tipo_item": "verso",
                **verso,
            }
            for verso in estrofa["versos"]
        )

    return items


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


def _obtener_tipos_rima_por_estrofa(
    palabras_finales_por_estrofa: list[list[str]],
    esquemas_rima_por_estrofa: list[dict],
) -> list[list[str]]:
    tipos_por_estrofa = []

    for palabras_finales, esquema_estrofa in zip(
        palabras_finales_por_estrofa,
        esquemas_rima_por_estrofa,
    ):
        esquema_rima = esquema_estrofa["esquema"]
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
        tipos_por_estrofa.append(tipos)

    return tipos_por_estrofa


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
