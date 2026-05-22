"""Learning concept list and detail components."""

import reflex as rx

from rimador.state import State
from rimador.styles.theme import (
    ACCENT_BACKGROUND,
    BORDER_RADIUS,
    PANEL_PADDING,
    TEXT_ON_ACCENT,
    borde_panel,
    color_texto_principal,
    color_texto_secundario,
    fondo_panel,
)


def item_concepto_aprender(concepto: dict) -> rx.Component:
    seleccionado = State.concepto_seleccionado == concepto["id"]
    return rx.button(
        rx.vstack(
            rx.text(
                concepto["titulo"],
                weight="bold",
                color=rx.cond(seleccionado, TEXT_ON_ACCENT, color_texto_principal()),
            ),
            rx.text(
                concepto["categoria"],
                size="2",
                color=rx.cond(seleccionado, "rgba(255,255,255,0.82)", color_texto_secundario()),
            ),
            spacing="1",
            align="start",
            width="100%",
        ),
        on_click=State.seleccionar_concepto(concepto["id"]),
        variant="soft",
        width="100%",
        justify_content="start",
        height="auto",
        padding=PANEL_PADDING,
        border=rx.cond(seleccionado, f"1px solid {ACCENT_BACKGROUND}", borde_panel()),
        border_radius=BORDER_RADIUS,
        background=rx.cond(seleccionado, ACCENT_BACKGROUND, fondo_panel()),
        color=rx.cond(seleccionado, TEXT_ON_ACCENT, color_texto_principal()),
    )


def lista_conceptos_aprender() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.cond(
                State.hay_conceptos_filtrados,
                rx.vstack(
                    rx.foreach(State.conceptos_filtrados, item_concepto_aprender),
                    spacing="2",
                    width="100%",
                ),
                rx.text("No se encontraron conceptos.", color=color_texto_secundario()),
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


def detalle_concepto_aprender() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.heading(State.concepto_actual["titulo"], size="6"),
                rx.badge(State.concepto_actual["categoria"]),
                spacing="3",
                align="center",
                wrap="wrap",
            ),
            rx.vstack(
                rx.text("Definición", weight="bold"),
                rx.text(State.concepto_actual["definicion"], color=color_texto_secundario()),
                spacing="1",
                align="start",
            ),
            rx.vstack(
                rx.text("Ejemplo", weight="bold"),
                rx.text(State.concepto_actual["ejemplo"], color=color_texto_secundario()),
                spacing="1",
                align="start",
            ),
            rx.vstack(
                rx.text("Cómo lo usa Rimador", weight="bold"),
                rx.text(State.concepto_actual["uso_en_rimador"], color=color_texto_secundario()),
                spacing="1",
                align="start",
            ),
            spacing="4",
            align="stretch",
        ),
        width="100%",
        padding=PANEL_PADDING,
        border=borde_panel(),
        border_radius=BORDER_RADIUS,
        background=fondo_panel(),
        color=color_texto_principal(),
    )


def item_concepto_aprender_expandible(concepto: dict) -> rx.Component:
    seleccionado = State.concepto_seleccionado == concepto["id"]
    return rx.vstack(
        item_concepto_aprender(concepto),
        rx.cond(
            seleccionado,
            detalle_concepto_aprender(),
            rx.box(),
        ),
        spacing="2",
        align="stretch",
        width="100%",
    )


def lista_conceptos_aprender_expandible() -> rx.Component:
    return rx.vstack(
        rx.cond(
            State.hay_conceptos_filtrados,
            rx.vstack(
                rx.foreach(
                    State.conceptos_filtrados,
                    item_concepto_aprender_expandible,
                ),
                spacing="3",
                width="100%",
            ),
            rx.card(
                rx.text(
                    "No se encontraron conceptos.",
                    color=color_texto_secundario(),
                ),
                width="100%",
                padding=PANEL_PADDING,
                border=borde_panel(),
                border_radius=BORDER_RADIUS,
                background=fondo_panel(),
                color=color_texto_principal(),
            ),
        ),
        spacing="3",
        align="stretch",
        width="100%",
    )
