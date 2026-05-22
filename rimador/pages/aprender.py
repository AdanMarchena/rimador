"""Learning page."""

import reflex as rx

from rimador.components.learn_concepts import (
    detalle_concepto_aprender,
    lista_conceptos_aprender,
)
from rimador.state import State
from rimador.styles.theme import (
    BORDER_RADIUS,
    borde_panel,
    color_texto_principal,
    fondo_panel,
)


def seccion_aprender() -> rx.Component:
    return rx.vstack(
        rx.heading("Aprender", size="7"),
        rx.input(
            placeholder="Buscar conceptos...",
            value=State.busqueda_aprender,
            on_change=State.buscar_conceptos,
            width="100%",
            border=borde_panel(),
            border_radius=BORDER_RADIUS,
            background=fondo_panel(),
            color=color_texto_principal(),
        ),
        rx.grid(
            lista_conceptos_aprender(),
            detalle_concepto_aprender(),
            columns="minmax(220px, 0.8fr) minmax(0, 1.4fr)",
            spacing="4",
            width="100%",
        ),
        spacing="4",
        align="stretch",
        width="100%",
    )
