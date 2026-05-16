"""Reflex entry point for the Rimador application."""

import reflex as rx


class State(rx.State):
    """Application state shared by the Reflex app."""


def index() -> rx.Component:
    """Render the initial page."""
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("Rimador", size="9"),
            rx.text("Herramienta inicial para analizar metrica y rima.", size="5"),
            spacing="5",
            justify="center",
            min_height="85vh",
        ),
    )


app = rx.App()
app.add_page(index)
