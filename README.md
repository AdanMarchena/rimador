# Rimador

Rimador es una herramienta gratuita y experimental para analizar escritura creativa en español. Su objetivo es ayudar a poetas, músicos, raperos, compositores y escritores a comprender mejor la métrica, la rima y el ritmo de sus textos.

Rimador busca unir tecnología, lingüística y creación artística en una herramienta accesible que permita no solo analizar textos, sino también aprender conceptos literarios y descubrir patrones que muchas veces pasan desapercibidos durante la escritura.

Actualmente el proyecto se encuentra en estado **beta**, por lo que algunas interpretaciones complejas del lenguaje todavía pueden requerir mejoras.

---

## Funciones actuales

### Análisis métrico

- Conteo de sílabas gramaticales
- Conteo de sílabas métricas
- Detección automática de sinalefas
- Ajuste por palabra aguda, llana y esdrújula
- Clasificación automática del tipo de verso
- Identificación de métrica predominante

### Análisis de rimas

- Detección de rima consonante
- Detección de rima asonante
- Detección de rimas internas
- Detección de patrones globales de rima
- Generación automática del esquema de rima (A, B, C...)

### Ritmo y estructura

- Detección de posiciones acentuadas
- Identificación de estructuras métricas
- Resumen global del texto

### Interfaz

- Editor de texto en tiempo real
- Vista analizada paralela
- Resaltado visual de rimas
- Modo claro y oscuro
- Sección educativa integrada
- Sección Acerca de
- Sistema de apoyo mediante donaciones

---

## Capturas

Próximamente se agregarán capturas de pantalla y ejemplos de uso.

---

## Tecnologías utilizadas

- Python
- Reflex
- Pytest

---

## Instalación

Clonar repositorio:

```bash
git clone https://github.com/AdanMarchena/rimador.git
```

Entrar al proyecto:

```bash
cd rimador
```

Crear entorno virtual:

```bash
python -m venv venv-rimador
```

Activar entorno virtual:

```bash
venv-rimador\Scripts\activate
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

---

## Ejecutar aplicación

```bash
reflex run
```

o

```bash
python -m reflex run
```

---

## Ejecutar pruebas

```bash
python -m pytest
```

---

## Filosofía del proyecto

Rimador no pretende reemplazar la intuición creativa ni dictar cómo debe escribirse una canción, una letra o un poema.

Su propósito es servir como apoyo técnico y educativo, ofreciendo una lectura estructurada del texto para ayudar a descubrir:

- patrones métricos
- relaciones sonoras
- estructuras rítmicas
- posibilidades creativas

El análisis debe entenderse como una ayuda y no como una autoridad absoluta.

---

## Limitaciones actuales

Esta versión beta todavía puede presentar errores en situaciones como:

- Hiato poético
- Sinéresis
- Diéresis
- Rimas complejas
- Interpretaciones expresivas
- Casos ambiguos del español
- Algunas rimas asonantes avanzadas

---

## Hoja de ruta

Próximas ideas:

- Más figuras literarias
- Enciclopedia literaria ampliada
- Mejoras de análisis rítmico
- Más visualizaciones
- Sugerencias creativas asistidas
- Exportación de análisis
- Estadísticas avanzadas
- Mejoras de precisión lingüística

---

## Apoyar el proyecto

Rimador es gratuito y se mantiene gracias al apoyo voluntario de personas que desean ayudar a su desarrollo.

Si la herramienta te resulta útil y quieres colaborar:

### ☕ Aporte libre

https://link.mercadopago.cl/biteroom

### CLP $1.000

https://mpago.la/29SRa9z

### CLP $5.000

https://mpago.la/1JeQaMT

### CLP $10.000

https://mpago.la/1osswVX

---

## Licencia

MIT License
