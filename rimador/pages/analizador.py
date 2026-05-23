"""Analyzer page."""

import reflex as rx

from rimador.components.analysis_cards import tarjetas_estrofa
from rimador.components.analysis_notices import aviso_formato_texto, aviso_texto_extenso
from rimador.components.analyzed_view import vista_analizada
from rimador.components.editor import editor_texto
from rimador.components.summary import panel_resumen
from rimador.state import State


def selector_layout_analizador() -> rx.Component:
    """Render desktop-only analyzer layout controls."""
    return rx.hstack(
        rx.button(
            "Horizontal",
            on_click=State.set_layout_horizontal,
            variant=rx.cond(
                State.layout_analizador == "horizontal",
                "solid",
                "soft",
            ),
            size="2",
            border_radius="8px",
        ),
        rx.button(
            "Vertical",
            on_click=State.set_layout_vertical,
            variant=rx.cond(
                State.layout_analizador == "vertical",
                "solid",
                "soft",
            ),
            size="2",
            border_radius="8px",
        ),
        spacing="2",
        align="center",
        display=rx.breakpoints(initial="none", md="flex"),
    )


def seccion_analizador() -> rx.Component:
    return rx.vstack(
        panel_resumen(),
        rx.hstack(
            selector_layout_analizador(),
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
        aviso_formato_texto(),
        aviso_texto_extenso(),
        rx.vstack(
            rx.flex(
                rx.box(
                    editor_texto(),
                    flex="1 1 0",
                    min_width="0",
                    width="100%",
                ),
                rx.box(
                    vista_analizada(),
                    flex="1 1 0",
                    min_width="0",
                    width="100%",
                ),
                direction=rx.breakpoints(
                    initial="column",
                    md=rx.cond(
                        State.layout_analizador == "horizontal",
                        "row",
                        "column",
                    ),
                ),
                spacing="3",
                align="stretch",
                width="100%",
            ),
            spacing="3",
            align="stretch",
            width="100%",
        ),
        rx.vstack(
            rx.foreach(State.estrofas_analisis, tarjetas_estrofa),
            spacing="4",
            width="100%",
        ),
        spacing="5",
        align="stretch",
        width="100%",
    )
