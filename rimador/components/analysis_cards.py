"""Detailed verse analysis cards."""

import reflex as rx

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
