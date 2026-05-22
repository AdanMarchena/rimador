"""Analyzed text view and syllable counters."""

import reflex as rx

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
    fondo_suave,
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


def vista_analizada() -> rx.Component:
    from rimador.state import State

    return rx.vstack(
        rx.heading("Vista analizada", size="5"),
        rx.grid(
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
                height=ANALYSIS_EDITOR_HEIGHT,
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
