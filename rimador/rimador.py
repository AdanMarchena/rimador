"""Reflex entry point for the Rimador application."""

import reflex as rx

from rimador.components.layout import layout_principal
from rimador.state import State
from rimador.styles.theme import FAVICON_SRC


def index() -> rx.Component:
    """Render the initial page."""
    return layout_principal()


app = rx.App(
    head_components=[
        rx.el.link(rel="icon", href=FAVICON_SRC, type="image/png"),
        rx.el.link(rel="shortcut icon", href=FAVICON_SRC, type="image/png"),
        rx.el.style(
            """
            .rimador-editor-textarea,
            .rimador-editor-textarea textarea,
            textarea.rimador-editor-textarea {
                line-height: 28px !important;
                font-size: 14px !important;
                font-family: monospace !important;
            }
            """
        ),
    ],
)
app.add_page(index, title="Rimador", image=FAVICON_SRC)
