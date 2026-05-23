"""Brand header."""

import reflex as rx

from rimador.styles.theme import LOGO_SRC


def encabezado_marca() -> rx.Component:
    return rx.box(
        rx.image(
            src=LOGO_SRC,
            alt="Logo de Rimador",
            height=rx.breakpoints(initial="120px", sm="260px", lg="360px"),
            width="auto",
            object_fit="contain",
            display="block",
            margin="0",
            transform=rx.breakpoints(
                initial="translateY(-8px)",
                sm="translateY(-36px)",
                lg="translateY(-58px)",
            ),
        ),
        height=rx.breakpoints(initial="98px", sm="190px", lg="235px"),
        overflow="hidden",
        padding_top="0.25rem",
        padding_bottom="0",
        margin="0",
    )
