"""Reflex entry point for the Rimador application."""

import reflex as rx

from core.metrica import analizar_metrica_verso
from core.rima import obtener_esquema_rima
from core.ritmo import obtener_posiciones_acentuadas_verso
from core.utils.texto import obtener_versos


class State(rx.State):
    """Application state shared by the Reflex app."""

    texto: str = ""
    resultados: list[dict] = []
    esquema_rima: list[str] = []

    def analizar(self, texto: str):
        """Analyze the entered text verse by verse."""
        self.texto = texto
        versos = obtener_versos(texto)
        self.esquema_rima = obtener_esquema_rima(versos)
        self.resultados = []

        for indice, verso in enumerate(versos):
            analisis = analizar_metrica_verso(verso)
            posiciones_acentuadas = obtener_posiciones_acentuadas_verso(verso)
            letra_rima = self.esquema_rima[indice] if indice < len(self.esquema_rima) else ""

            self.resultados.append(
                {
                    "texto": analisis["verso"],
                    "silabas_gramaticales": analisis["silabas_gramaticales"],
                    "silabas_metricas": analisis["silabas_metricas"],
                    "sinalefas": _formatear_sinalefas(analisis["sinalefas"]),
                    "ajuste_final": analisis["ajuste_final"],
                    "posiciones_acentuadas": posiciones_acentuadas,
                    "posiciones_acentuadas_texto": str(posiciones_acentuadas),
                    "letra_rima": letra_rima,
                }
            )


def _formatear_sinalefas(sinalefas: list[dict]) -> str:
    if not sinalefas:
        return "ninguna"

    return ", ".join(
        f"{sinalefa['anterior']} + {sinalefa['siguiente']}"
        for sinalefa in sinalefas
    )


def _fila_resultado(etiqueta: str, valor: rx.Var) -> rx.Component:
    return rx.hstack(
        rx.text(etiqueta, weight="bold"),
        rx.text(valor),
        spacing="2",
        align="start",
    )


def tarjeta_verso(resultado: dict) -> rx.Component:
    """Render one verse analysis card."""
    return rx.card(
        rx.vstack(
            rx.text(resultado["texto"], weight="bold", size="4"),
            _fila_resultado("Sílabas gramaticales:", resultado["silabas_gramaticales"]),
            _fila_resultado("Sílabas métricas:", resultado["silabas_metricas"]),
            _fila_resultado("Sinalefas detectadas:", resultado["sinalefas"]),
            _fila_resultado("Ajuste final:", resultado["ajuste_final"]),
            _fila_resultado(
                "Posiciones acentuadas:",
                resultado["posiciones_acentuadas_texto"],
            ),
            _fila_resultado("Esquema de rima:", resultado["letra_rima"]),
            spacing="2",
            align="start",
        ),
        width="100%",
    )


def index() -> rx.Component:
    """Render the initial page."""
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("Rimador", size="9"),
            rx.text("Analiza métrica, ritmo básico y rima verso a verso.", size="5"),
            rx.text_area(
                placeholder="Escribe un poema o varios versos...",
                value=State.texto,
                on_change=State.analizar,
                width="100%",
                min_height="12rem",
            ),
            rx.vstack(
                rx.foreach(State.resultados, tarjeta_verso),
                spacing="4",
                width="100%",
            ),
            spacing="5",
            align="stretch",
            width="100%",
        ),
        max_width="900px",
        padding_y="3rem",
    )


app = rx.App()
app.add_page(index)
