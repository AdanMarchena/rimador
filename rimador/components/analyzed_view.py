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

ANALYZED_ROW_HEIGHT = "28px"


def vista_rima_verso(resultado: dict) -> rx.Component:
    """Render one verse with its rhyme fragment highlighted."""
    from rimador.state import State

    return rx.hstack(
        rx.box(
            rx.html(resultado["html_vista_rima"]),
            flex="1",
            min_width="0",
            width="100%",
            white_space="normal",
            overflow_wrap="break-word",
            min_height=EDITOR_LINE_HEIGHT,
            line_height=EDITOR_LINE_HEIGHT,
        ),
        rx.box(
            rx.cond(
                resultado["letra_rima"] != "",
                rx.text(
                    resultado["letra_rima"],
                    size="1",
                    weight="bold",
                    display="flex",
                    align_items="center",
                    justify_content="center",
                    height="100%",
                    line_height="1",
                    margin="0",
                    padding="0",
                    white_space="nowrap",
                ),
                rx.box(),
            ),
            display="flex",
            align_items="center",
            justify_content="center",
            width="32px",
            min_width="32px",
            max_width="32px",
            flex_shrink="0",
            height=ANALYZED_ROW_HEIGHT,
            min_height=ANALYZED_ROW_HEIGHT,
            border="1px solid",
            border_color=rx.cond(
                State.modo_visualizacion == "ritmo",
                rx.cond(resultado["letra_rima"] != "", "#64748B", "transparent"),
                resultado["letra_rima_border"],
            ),
            border_radius="999px",
            background=rx.cond(
                State.modo_visualizacion == "ritmo",
                rx.cond(resultado["letra_rima"] != "", "#E2E8F0", "transparent"),
                resultado["letra_rima_background"],
            ),
            color=rx.cond(
                State.modo_visualizacion == "ritmo",
                rx.cond(resultado["letra_rima"] != "", "#1E293B", "transparent"),
                resultado["letra_rima_text"],
            ),
            line_height=ANALYZED_ROW_HEIGHT,
            white_space="nowrap",
            overflow="hidden",
        ),
        display="flex",
        align_items="center",
        spacing="2",
        margin="0",
        padding="0",
        height=ANALYZED_ROW_HEIGHT,
        min_height=ANALYZED_ROW_HEIGHT,
        line_height=ANALYZED_ROW_HEIGHT,
        width="100%",
        min_width="0",
        wrap="nowrap",
    )


def aviso_ritmo_en_desarrollo() -> rx.Component:
    """Render a temporary honest message for rhythm mode."""
    return rx.vstack(
        rx.text(
            "Análisis rítmico avanzado en desarrollo.",
            weight="bold",
            size="3",
        ),
        rx.text(
            "Por ahora Rimador calcula posiciones acentuales básicas, pero la detección de acentos rítmicos relevantes requiere una versión más precisa.",
            color="#64748B",
            line_height="1.5",
        ),
        spacing="2",
        align="start",
        width="100%",
        padding="12px",
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
        height=ANALYZED_ROW_HEIGHT,
        min_height=ANALYZED_ROW_HEIGHT,
        margin="0",
        padding="0",
        line_height=ANALYZED_ROW_HEIGHT,
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
        rx.hstack(
            rx.heading("Vista analizada", size="5"),
            rx.hstack(
                rx.button(
                    "Rimas",
                    on_click=State.set_modo_rimas,
                    variant=rx.cond(
                        State.modo_visualizacion == "rimas",
                        "solid",
                        "soft",
                    ),
                    size="2",
                    border_radius="8px",
                ),
                rx.button(
                    "Ritmo",
                    on_click=State.set_modo_ritmo,
                    variant=rx.cond(
                        State.modo_visualizacion == "ritmo",
                        "solid",
                        "soft",
                    ),
                    size="2",
                    border_radius="8px",
                ),
                spacing="2",
                align="center",
            ),
            justify="between",
            align="center",
            wrap="wrap",
            min_height="32px",
            width="100%",
        ),
        rx.grid(
            rx.box(
                rx.cond(
                    State.modo_visualizacion == "ritmo",
                    aviso_ritmo_en_desarrollo(),
                    rx.vstack(
                        rx.foreach(State.lineas_vista, vista_rima_verso),
                        spacing="0",
                        align="start",
                        width="100%",
                    ),
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
                background=fondo_panel(),
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
