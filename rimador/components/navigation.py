"""Top navigation controls."""

import reflex as rx

from rimador.state import State
from rimador.styles.theme import TEXT_ON_ACCENT, color_texto_principal


def boton_navegacion(etiqueta: str, seccion: str, accion) -> rx.Component:
    return rx.button(
        etiqueta,
        on_click=accion,
        variant=rx.cond(State.seccion_actual == seccion, "solid", "soft"),
        size="2",
        border_radius="10px",
        color=rx.cond(
            State.seccion_actual == seccion,
            TEXT_ON_ACCENT,
            color_texto_principal(),
        ),
    )


def menu_superior() -> rx.Component:
    return rx.hstack(
        boton_navegacion("Analizador", "analizador", State.mostrar_analizador),
        boton_navegacion("Aprender", "aprender", State.mostrar_aprender),
        boton_navegacion("Acerca de", "acerca_de", State.mostrar_acerca_de),
        spacing="3",
        align="center",
        wrap="wrap",
    )
