"""About page."""

import reflex as rx

from rimador.components.donations import boton_donacion_acerca
from rimador.styles.theme import (
    BORDER_RADIUS,
    PANEL_PADDING,
    borde_panel,
    color_texto_principal,
    color_texto_secundario,
    fondo_panel,
)


def seccion_acerca_de() -> rx.Component:
    return rx.vstack(
        rx.heading("Acerca de", size="7"),
        rx.card(
            rx.vstack(
                rx.text(
                    "Rimador es una herramienta gratuita y experimental para analizar escritura creativa en español. Su objetivo es ayudar a poetas, músicos, raperos, compositores y escritores a comprender mejor la métrica, la rima y el ritmo de sus textos.",
                    color=color_texto_secundario(),
                ),
                rx.text(
                    "El proyecto busca unir tecnología, lingüística y creación artística en una herramienta accesible. Rimador no pretende reemplazar la intuición creativa ni dictar cómo debe escribirse un poema o una canción, sino ofrecer una lectura técnica que ayude a descubrir patrones, posibilidades y detalles del texto.",
                    color=color_texto_secundario(),
                ),
                rx.text(
                    "Esta versión beta puede cometer errores, especialmente en casos interpretativos como hiato poético, sinéresis, diéresis, licencias expresivas o rimas complejas. Por eso, los resultados deben entenderse como una ayuda orientativa, no como una sentencia absoluta.",
                    color=color_texto_secundario(),
                ),
                rx.text(
                    "Rimador es gratuito. Si la herramienta te resulta útil y quieres apoyar su desarrollo, puedes realizar una donación voluntaria. Ese apoyo ayuda a mantener el proyecto, mejorar los análisis y agregar nuevo contenido educativo.",
                    color=color_texto_secundario(),
                ),
                boton_donacion_acerca(),
                spacing="3",
                align="start",
            ),
            width="100%",
            padding=PANEL_PADDING,
            border=borde_panel(),
            border_radius=BORDER_RADIUS,
            background=fondo_panel(),
            color=color_texto_principal(),
        ),
        spacing="4",
        align="stretch",
        width="100%",
    )
