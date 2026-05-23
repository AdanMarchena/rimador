"""Editor panel for the analyzer."""

import reflex as rx

from rimador.components.analyzed_view import contador_silabas_gramaticales
from rimador.state import State
from rimador.styles.theme import (
    ANALYSIS_COUNTER_COLUMNS,
    ANALYSIS_EDITOR_HEIGHT,
    BORDER_RADIUS,
    EDITOR_FONT_SIZE,
    EDITOR_LINE_HEIGHT,
    EDITOR_PADDING,
    borde_panel,
    color_texto_principal,
    fondo_panel,
)


def editor_texto() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.heading("Escribe tu texto", size="5"),
            align="center",
            min_height="32px",
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
                height=ANALYSIS_EDITOR_HEIGHT,
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
                height=ANALYSIS_EDITOR_HEIGHT,
                padding_y=EDITOR_PADDING,
                overflow_y="auto",
            ),
            columns=ANALYSIS_COUNTER_COLUMNS,
            spacing="3",
            width="100%",
        ),
        spacing="3",
        align="stretch",
        width="100%",
        min_width="0",
        flex="1",
    )
