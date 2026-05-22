"""Shared visual constants and theme helpers for Rimador."""

import reflex as rx


EDITOR_FONT_SIZE = "14px"
EDITOR_LINE_HEIGHT = "22px"
EDITOR_PADDING = "16px"
INLINE_RHYME_HEIGHT = "18px"
ANALYSIS_COUNTER_COLUMNS = "minmax(0, 1fr) 42px"
ANALYSIS_EDITOR_HEIGHT = ["360px", "420px", "500px"]
BORDER_RADIUS = "12px"
BORDER_COLOR = "#D9DEE8"
BORDER = f"1px solid {BORDER_COLOR}"
PANEL_BACKGROUND = "#FFFFFF"
SOFT_BACKGROUND = "#F8FAFC"
PANEL_PADDING = "16px"
TEXT_PRIMARY = "#1F2328"
TEXT_SECONDARY = "#4B5563"
TEXT_ON_ACCENT = "#FFFFFF"
TEXT_PRIMARY_DARK = "#F8FAFC"
TEXT_SECONDARY_DARK = "#CBD5E1"
CARD_BACKGROUND = "#FFFFFF"
CARD_BACKGROUND_DARK = "#1E293B"
CARD_BORDER = "#D9DEE8"
CARD_BORDER_DARK = "#334155"
ACCENT_BACKGROUND = "#0F8BEF"
ACCENT_BACKGROUND_SOFT = "#E8F3FE"
LOGO_SRC = "/logo/logo.png"
FAVICON_SRC = "/favicon.png"


def color_texto_principal():
    return rx.color_mode_cond(TEXT_PRIMARY, TEXT_PRIMARY_DARK)


def color_texto_secundario():
    return rx.color_mode_cond(TEXT_SECONDARY, TEXT_SECONDARY_DARK)


def fondo_panel():
    return rx.color_mode_cond(CARD_BACKGROUND, CARD_BACKGROUND_DARK)


def fondo_suave():
    return rx.color_mode_cond(SOFT_BACKGROUND, "#0F172A")


def borde_panel():
    return rx.color_mode_cond(
        f"1px solid {CARD_BORDER}",
        f"1px solid {CARD_BORDER_DARK}",
    )
