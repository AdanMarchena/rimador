"""Release notes dialog and changelog components."""

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
from rimador.version import APP_VERSION, NOVEDADES


def lista_novedades() -> rx.Component:
    return rx.vstack(
        *[
            rx.hstack(
                rx.text("•", color=color_texto_secundario()),
                rx.text(novedad, color=color_texto_principal()),
                spacing="2",
                align="start",
            )
            for novedad in NOVEDADES
        ],
        spacing="2",
        align="stretch",
        width="100%",
    )


def modal_novedades() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.vstack(
                rx.heading(f"Novedades de Rimador {APP_VERSION}", size="5"),
                rx.text(
                    "Esta versión incluye estas mejoras:",
                    color=color_texto_secundario(),
                ),
                lista_novedades(),
                rx.button(
                    "Entendido",
                    on_click=State.cerrar_novedades,
                    border_radius="10px",
                ),
                spacing="4",
                align="stretch",
            ),
            max_width="420px",
            border=borde_panel(),
            border_radius=BORDER_RADIUS,
            background=fondo_panel(),
            color=color_texto_principal(),
        ),
        open=State.mostrar_modal_novedades,
    )


def historial_novedades() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.heading("Novedades", size="5"),
            rx.text(f"Versión {APP_VERSION}", weight="bold", color=color_texto_principal()),
            lista_novedades(),
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
