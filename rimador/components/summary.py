"""Summary components for the analyzer."""

import reflex as rx

from rimador.state import State
from rimador.styles.theme import (
    BORDER_RADIUS,
    PANEL_PADDING,
    borde_panel,
    color_texto_principal,
    color_texto_secundario,
    fondo_panel,
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
