"""Complete analysis page for long texts."""

import reflex as rx

from rimador.components.help_tooltip import etiqueta_con_ayuda
from rimador.state import State
from rimador.styles.theme import (
    BORDER_RADIUS,
    PANEL_PADDING,
    borde_panel,
    color_texto_principal,
    color_texto_secundario,
    fondo_panel,
    fondo_suave,
)


def _encabezado_estrofa(item: dict) -> rx.Component:
    return rx.card(
        rx.hstack(
            rx.heading("Estrofa ", item["numero"], size="5"),
            rx.badge(item["esquema_texto"]),
            spacing="3",
            align="center",
            wrap="wrap",
        ),
        width="100%",
        padding=PANEL_PADDING,
        border=borde_panel(),
        border_radius=BORDER_RADIUS,
        background=fondo_panel(),
        color=color_texto_principal(),
    )


def _dato_verso(titulo: str, clave_ayuda: str, valor: rx.Component) -> rx.Component:
    return rx.vstack(
        etiqueta_con_ayuda(
            titulo,
            clave_ayuda,
            size="2",
            color=color_texto_secundario(),
        ),
        valor,
        spacing="1",
        align="start",
    )


def _dato_arte_verso(resultado: dict) -> rx.Component:
    return rx.cond(
        resultado["arte_verso"] == "arte menor",
        _dato_verso(
            "Arte",
            "arte_menor",
            rx.text(resultado["arte_verso"], weight="bold"),
        ),
        rx.cond(
            resultado["arte_verso"] == "arte mayor",
            _dato_verso(
                "Arte",
                "arte_mayor",
                rx.text(resultado["arte_verso"], weight="bold"),
            ),
            rx.vstack(
                rx.text("Arte", size="2", color=color_texto_secundario()),
                rx.text(resultado["arte_verso"], weight="bold"),
                spacing="1",
                align="start",
            ),
        ),
    )


def _fila_verso_completo(resultado: dict) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.box(
                rx.html(resultado["html_vista_rima"]),
                width="100%",
                padding="12px",
                border=borde_panel(),
                border_radius=BORDER_RADIUS,
                background=fondo_suave(),
                color=color_texto_principal(),
            ),
            rx.grid(
                _dato_verso(
                    "Sílabas gramaticales",
                    "silabas_gramaticales",
                    rx.text(resultado["silabas_gramaticales"], weight="bold"),
                ),
                _dato_verso(
                    "Sílabas métricas",
                    "silabas_metricas",
                    rx.text(resultado["silabas_metricas"], weight="bold"),
                ),
                _dato_verso(
                    "Tipo de verso",
                    "tipo_verso",
                    rx.badge(resultado["tipo_verso"]),
                ),
                _dato_arte_verso(resultado),
                rx.vstack(
                    rx.cond(
                        resultado["tipo_rima"] == "consonante",
                        etiqueta_con_ayuda(
                            "Rima final",
                            "rima_consonante",
                            size="2",
                            color=color_texto_secundario(),
                        ),
                        rx.cond(
                            resultado["tipo_rima"] == "asonante",
                            etiqueta_con_ayuda(
                                "Rima final",
                                "rima_asonante",
                                size="2",
                                color=color_texto_secundario(),
                            ),
                            rx.text("Rima final", size="2", color=color_texto_secundario()),
                        ),
                    ),
                    rx.hstack(
                        rx.badge(resultado["letra_rima"]),
                        rx.text(resultado["tipo_rima"]),
                        spacing="2",
                        align="center",
                    ),
                    spacing="1",
                    align="start",
                ),
                columns="repeat(auto-fit, minmax(150px, 1fr))",
                spacing="3",
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


def _resumen_grupos_rima(item: dict) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.text("Grupos de rimas", weight="bold"),
            rx.text(
                item["grupos_rima_texto"],
                white_space="pre-line",
                line_height="1.7",
                color=color_texto_principal(),
            ),
            spacing="2",
            align="stretch",
        ),
        width="100%",
        padding=PANEL_PADDING,
        border=borde_panel(),
        border_radius=BORDER_RADIUS,
        background=fondo_panel(),
        color=color_texto_principal(),
    )


def _estrofa_completa(estrofa: dict) -> rx.Component:
    return rx.vstack(
        _encabezado_estrofa(estrofa),
        rx.foreach(estrofa["versos"], _fila_verso_completo),
        _resumen_grupos_rima(estrofa),
        spacing="3",
        align="stretch",
        width="100%",
    )


def seccion_analisis_completo() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.heading("Análisis completo", size="7"),
            rx.button(
                "Volver al analizador",
                on_click=State.mostrar_analizador,
                variant="soft",
                border_radius="10px",
            ),
            rx.button(
                "Exportar PDF",
                on_click=State.exportar_pdf,
                border_radius="10px",
            ),
            justify="between",
            align="center",
            wrap="wrap",
            width="100%",
        ),
        rx.vstack(
            rx.foreach(State.estrofas_analisis, _estrofa_completa),
            spacing="4",
            align="stretch",
            width="100%",
        ),
        spacing="4",
        align="stretch",
        width="100%",
    )
