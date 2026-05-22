"""Summary components for the analyzer."""

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
)


def _resumen_item(etiqueta: str, valor: rx.Var) -> rx.Component:
    return rx.vstack(
        rx.text(etiqueta, size="2", color=color_texto_secundario()),
        rx.text(valor, weight="bold", color=color_texto_principal()),
        spacing="1",
        align="start",
    )


def _resumen_item_ayuda(
    etiqueta: str,
    clave_ayuda: str,
    valor: rx.Var,
) -> rx.Component:
    return rx.vstack(
        etiqueta_con_ayuda(
            etiqueta,
            clave_ayuda,
            size="2",
            color=color_texto_secundario(),
        ),
        rx.text(valor, weight="bold", color=color_texto_principal()),
        spacing="1",
        align="start",
    )


def _resumen_esquema_item(esquema: dict) -> rx.Component:
    return rx.hstack(
        rx.text(esquema["etiqueta"], size="2", color=color_texto_secundario()),
        rx.text(esquema["esquema"], weight="bold", color=color_texto_principal()),
        spacing="2",
        align="start",
        wrap="wrap",
    )


def panel_resumen() -> rx.Component:
    """Render the text-level metric and rhyme summary."""
    return rx.card(
        rx.vstack(
            rx.heading("Resumen", size="4"),
            rx.grid(
                _resumen_item("Versos totales", State.resumen_cantidad_versos),
                _resumen_item("Estrofas", State.resumen_cantidad_estrofas),
                _resumen_item_ayuda(
                    "Métrica predominante",
                    "tipo_verso",
                    State.resumen_tipo_predominante,
                ),
                _resumen_item("Regularidad", State.resumen_regularidad),
                columns="repeat(auto-fit, minmax(160px, 1fr))",
                spacing="4",
                width="100%",
            ),
            rx.vstack(
                rx.text("Esquemas de rima", size="2", color=color_texto_secundario()),
                rx.vstack(
                    rx.foreach(State.resumen_esquemas_rima, _resumen_esquema_item),
                    spacing="1",
                    align="stretch",
                    width="100%",
                ),
                spacing="1",
                align="stretch",
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
