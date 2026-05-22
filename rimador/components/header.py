"""Brand header."""

import reflex as rx

from rimador.styles.theme import LOGO_SRC


def encabezado_marca() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.image(
                src=LOGO_SRC,
                alt="Logo de Rimador",
                height="60px",
                width="90px",
                object_fit="cover",
                object_position="32% 50%",
                border_radius="10px",
            ),
            rx.heading("Rimador", size="9"),
            spacing="3",
            align="center",
        ),
        rx.text(
            "Analiza métrica, ritmo básico y rima verso a verso.",
            size="5",
        ),
        spacing="2",
        align="start",
    )
