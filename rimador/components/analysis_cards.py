"""Detailed verse analysis cards."""

import reflex as rx

from rimador.components.help_tooltip import etiqueta_con_ayuda
from rimador.styles.theme import (
    BORDER_RADIUS,
    PANEL_PADDING,
    borde_panel,
    color_texto_principal,
    fondo_panel,
)


def _fila_resultado(etiqueta: str, valor: rx.Var) -> rx.Component:
    return rx.hstack(
        rx.text(etiqueta, weight="bold"),
        rx.text(valor),
        spacing="2",
        align="start",
    )


def _fila_resultado_ayuda(
    etiqueta: str,
    clave_ayuda: str,
    valor: rx.Var,
) -> rx.Component:
    return rx.hstack(
        etiqueta_con_ayuda(etiqueta, clave_ayuda, weight="bold"),
        rx.text(valor),
        spacing="2",
        align="start",
        wrap="wrap",
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


def _etiqueta_tipo_rima(resultado: dict) -> rx.Component:
    return rx.cond(
        resultado["tipo_rima"] == "consonante",
        etiqueta_con_ayuda("Tipo:", "rima_consonante", weight="bold"),
        rx.cond(
            resultado["tipo_rima"] == "asonante",
            etiqueta_con_ayuda("Tipo:", "rima_asonante", weight="bold"),
            rx.text("Tipo:", weight="bold"),
        ),
    )


def _etiqueta_arte_verso(resultado: dict) -> rx.Component:
    return rx.cond(
        resultado["arte_verso"] == "arte menor",
        etiqueta_con_ayuda("Arte:", "arte_menor", weight="bold"),
        rx.cond(
            resultado["arte_verso"] == "arte mayor",
            etiqueta_con_ayuda("Arte:", "arte_mayor", weight="bold"),
            rx.text("Arte:", weight="bold"),
        ),
    )


def tarjeta_verso(resultado: dict) -> rx.Component:
    """Render one verse analysis card."""
    return rx.card(
        rx.vstack(
            rx.text(resultado["texto"], weight="bold", size="4"),
            _fila_resultado_ayuda(
                "Sílabas gramaticales:",
                "silabas_gramaticales",
                resultado["silabas_gramaticales"],
            ),
            rx.hstack(
                etiqueta_con_ayuda(
                    "Sílabas métricas:",
                    "silabas_metricas",
                    weight="bold",
                ),
                rx.text(resultado["silabas_metricas"]),
                rx.badge(resultado["tipo_verso"]),
                spacing="2",
                align="center",
                wrap="wrap",
            ),
            rx.hstack(
                _etiqueta_arte_verso(resultado),
                rx.text(resultado["arte_verso"]),
                spacing="2",
                align="start",
                wrap="wrap",
            ),
            _fila_resultado_ayuda(
                "Sinalefas detectadas:",
                "sinalefas",
                resultado["sinalefas"],
            ),
            _fila_resultado_ayuda(
                "Ajuste final:",
                "ajuste_final",
                resultado["ajuste_final"],
            ),
            _fila_resultado_ayuda(
                "Posiciones acentuadas:",
                "posiciones_acentuadas",
                resultado["posiciones_acentuadas_texto"],
            ),
            _fila_resultado("Última palabra:", resultado["ultima_palabra"]),
            rx.hstack(
                rx.text("Fragmento rimante:", weight="bold"),
                rx.badge(resultado["fragmento_rimante"]),
                spacing="2",
                align="start",
            ),
            rx.hstack(
                _etiqueta_tipo_rima(resultado),
                rx.text(resultado["tipo_rima"]),
                spacing="2",
                align="start",
                wrap="wrap",
            ),
            _fila_resultado("Esquema de rima:", resultado["letra_rima"]),
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

def tarjeta_grupos_rima(estrofa: dict) -> rx.Component:
    """Render rhyme groups after all verses in one stanza."""
    return rx.card(
        rx.vstack(
            rx.text("Grupos de rimas", weight="bold", size="4"),
            rx.cond(
                estrofa["tiene_grupos_rima"],
                rx.text(
                    estrofa["grupos_rima_texto"],
                    white_space="pre-line",
                ),
                rx.text("Sin grupos de rima detectados"),
            ),
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


def tarjetas_estrofa(estrofa: dict) -> rx.Component:
    """Render all verse cards in a stanza and then its rhyme groups."""
    return rx.vstack(
        rx.text(
            f"Estrofa {estrofa['numero']}",
            weight="bold",
            size="5",
        ),
        rx.foreach(estrofa["versos"], tarjeta_verso),
        tarjeta_grupos_rima(estrofa),
        spacing="4",
        width="100%",
        align="stretch",
    )