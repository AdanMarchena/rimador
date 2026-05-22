"""Analyzer notices for formatting and long text."""

import reflex as rx

from rimador.state import State
from rimador.styles.theme import (
    ACCENT_BACKGROUND_SOFT,
    BORDER_RADIUS,
    PANEL_PADDING,
    borde_panel,
    color_texto_principal,
)


def aviso_formato_texto() -> rx.Component:
    return rx.cond(
        State.mostrar_advertencia_formato,
        rx.box(
            rx.text(
                "Rimador analiza cada salto de línea como un verso. Para mejores resultados, organiza tu texto con un verso por línea.",
                color=color_texto_principal(),
            ),
            width="100%",
            padding=PANEL_PADDING,
            border=borde_panel(),
            border_radius=BORDER_RADIUS,
            background=ACCENT_BACKGROUND_SOFT,
        ),
        rx.box(),
    )


def aviso_texto_extenso() -> rx.Component:
    return rx.cond(
        State.texto_extenso,
        rx.hstack(
            rx.text(
                "Texto extenso detectado. Para una lectura más clara, usa Análisis completo.",
                color=color_texto_principal(),
            ),
            rx.button(
                "Ver análisis completo",
                on_click=State.mostrar_analisis_completo,
                border_radius="10px",
            ),
            spacing="3",
            align="center",
            justify="between",
            wrap="wrap",
            width="100%",
            padding=PANEL_PADDING,
            border=borde_panel(),
            border_radius=BORDER_RADIUS,
            background=ACCENT_BACKGROUND_SOFT,
        ),
        rx.box(),
    )
