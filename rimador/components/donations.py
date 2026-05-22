"""Donation panel and floating button."""

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


DONATION_URL = "https://link.mercadopago.cl/biteroom"
DONATION_OPTIONS = [
    ("☕ Aporte libre", "https://link.mercadopago.cl/biteroom"),
    ("CLP $1.000", "https://mpago.la/29SRa9z"),
    ("CLP $5.000", "https://mpago.la/1JeQaMT"),
    ("CLP $10.000", "https://mpago.la/1osswVX"),
]


def opcion_donacion(etiqueta: str, url: str) -> rx.Component:
    return rx.link(
        rx.button(
            etiqueta,
            variant="soft",
            width="100%",
            justify_content="start",
            border_radius="10px",
            color=color_texto_principal(),
        ),
        href=url,
        is_external=True,
        width="100%",
    )


def panel_donacion() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.heading("Apoya el proyecto", size="4", color=color_texto_principal()),
                rx.spacer(),
                rx.button(
                    "×",
                    on_click=State.cerrar_panel_donacion,
                    variant="soft",
                    border_radius="999px",
                    cursor="pointer",
                ),
                width="100%",
                align="center",
            ),
            rx.text(
                "Rimador es gratuito y se mantiene gracias al apoyo voluntario de personas que desean ayudar a su desarrollo.",
                color=color_texto_secundario(),
            ),
            rx.vstack(
                *[
                    opcion_donacion(etiqueta, url)
                    for etiqueta, url in DONATION_OPTIONS
                ],
                spacing="2",
                width="100%",
            ),
            spacing="3",
            align="stretch",
            width="100%",
        ),
        position="fixed",
        bottom="84px",
        right="24px",
        width="300px",
        padding=PANEL_PADDING,
        border=borde_panel(),
        border_radius=BORDER_RADIUS,
        background=fondo_panel(),
        box_shadow="0 18px 48px rgba(15, 23, 42, 0.24)",
        z_index="1000",
    )


def boton_donacion_flotante() -> rx.Component:
    return rx.vstack(
        rx.cond(State.panel_donacion_abierto, panel_donacion(), rx.box()),
        rx.button(
            "❤️ Apoyar Rimador",
            on_click=State.alternar_panel_donacion,
            background=ACCENT_BACKGROUND,
            color=TEXT_ON_ACCENT,
            border_radius="999px",
            padding_x="18px",
            box_shadow="0 10px 24px rgba(15, 139, 239, 0.28)",
            cursor="pointer",
            title="Apoya el desarrollo de Rimador",
        ),
        align="end",
        spacing="2",
    )


def boton_donacion_acerca() -> rx.Component:
    return rx.button(
        "Apoyar con una donación",
        background=ACCENT_BACKGROUND,
        color=TEXT_ON_ACCENT,
        border_radius="10px",
        on_click=State.abrir_panel_donacion,
    )
