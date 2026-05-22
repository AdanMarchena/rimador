"""Analyzer page."""

import reflex as rx

from rimador.components.analysis_cards import tarjeta_verso
from rimador.components.analyzed_view import vista_analizada
from rimador.components.editor import editor_texto
from rimador.components.summary import panel_resumen
from rimador.state import State


def seccion_analizador() -> rx.Component:
    return rx.vstack(
        panel_resumen(),
        rx.vstack(
            rx.flex(
                editor_texto(),
                vista_analizada(),
                direction=rx.breakpoints(initial="column", md="row"),
                spacing="3",
                align="stretch",
                width="100%",
            ),
            spacing="3",
            align="stretch",
            width="100%",
        ),
        rx.vstack(
            rx.foreach(State.resultados, tarjeta_verso),
            spacing="4",
            width="100%",
        ),
        spacing="5",
        align="stretch",
        width="100%",
    )
