"""Reflex entry point for the Rimador application."""

import reflex as rx

from rimador.components.layout import layout_principal
from rimador.styles.theme import FAVICON_SRC


def index() -> rx.Component:
    """Render the initial page."""
    return layout_principal()


app = rx.App()
app.add_page(index, title="Rimador", image=FAVICON_SRC)
