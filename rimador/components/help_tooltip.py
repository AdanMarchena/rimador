"""Contextual help tooltip components."""

import reflex as rx

from rimador.data.ayuda import AYUDA_TERMINOS
from rimador.state import State
from rimador.styles.theme import (
    BORDER_RADIUS,
    PANEL_PADDING,
    TEXT_ON_ACCENT,
    borde_panel,
    color_texto_principal,
    color_texto_secundario,
    fondo_panel,
)


def help_tooltip(
    titulo: str,
    definicion: str,
    ejemplo: str = "",
    concepto_id: str = "",
) -> rx.Component:
    contenido = rx.vstack(
        rx.text(titulo, weight="bold", color=color_texto_principal()),
        rx.text(definicion, size="2", color=color_texto_secundario()),
        rx.cond(
            ejemplo != "",
            rx.text(ejemplo, size="2", color=color_texto_secundario()),
            rx.box(),
        ),
        rx.button(
            "Ver más en Aprender",
            size="1",
            variant="soft",
            border_radius="8px",
            on_click=State.ver_concepto_aprender(concepto_id),
        ),
        spacing="2",
        align="start",
        max_width="260px",
        padding=PANEL_PADDING,
    )

    return rx.popover.root(
        rx.popover.trigger(
            rx.button(
                "ⓘ",
                size="1",
                variant="soft",
                width="22px",
                height="22px",
                min_width="22px",
                border_radius="999px",
                padding="0",
                cursor="pointer",
                aria_label=f"Información: {titulo}",
            )
        ),
        rx.popover.content(
            contenido,
            width="280px",
            border=borde_panel(),
            border_radius=BORDER_RADIUS,
            background=fondo_panel(),
            color=color_texto_principal(),
        ),
    )


def ayuda_termino(clave: str) -> rx.Component:
    ayuda = AYUDA_TERMINOS[clave]
    return help_tooltip(
        ayuda["titulo"],
        ayuda["definicion"],
        ayuda.get("ejemplo", ""),
        ayuda.get("concepto_id", ""),
    )


def etiqueta_con_ayuda(texto: str, clave: str, **text_props) -> rx.Component:
    return rx.hstack(
        rx.text(texto, **text_props),
        ayuda_termino(clave),
        spacing="1",
        align="center",
        wrap="nowrap",
    )
