"""Application layout composition."""

import reflex as rx

from rimador.components.donations import boton_donacion_flotante
from rimador.components.header import encabezado_marca
from rimador.components.navigation import menu_superior
from rimador.pages.acerca import seccion_acerca_de
from rimador.pages.analisis_completo import seccion_analisis_completo
from rimador.pages.analizador import seccion_analizador
from rimador.pages.aprender import seccion_aprender
from rimador.state import State


def contenido_actual() -> rx.Component:
    return rx.cond(
        State.seccion_actual == "aprender",
        seccion_aprender(),
        rx.cond(
            State.seccion_actual == "acerca_de",
            seccion_acerca_de(),
            rx.cond(
                State.seccion_actual == "analisis_completo",
                seccion_analisis_completo(),
                seccion_analizador(),
            ),
        ),
    )


def layout_principal() -> rx.Component:
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.box(
            boton_donacion_flotante(),
            position="fixed",
            right="24px",
            bottom="80px",
            z_index="999",
            cursor="pointer",
        ),
        rx.vstack(
            rx.hstack(
                encabezado_marca(),
                menu_superior(),
                justify="between",
                align="center",
                width="100%",
                wrap="wrap",
                spacing="4",
            ),
            contenido_actual(),
            spacing="1",
            align="stretch",
            width="100%",
        ),
        max_width="1200px",
        padding_top="0.25rem",
        padding_bottom="2rem",
    )
