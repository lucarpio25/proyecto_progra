# Dashboard del Catálogo de Netflix

## Descripción

Este proyecto corresponde a la entrega parcial del curso Programación Avanzada para la Ciencia de Datos.

La aplicación fue desarrollada en Streamlit y permite analizar un dataset del catálogo de Netflix mediante filtros interactivos, métricas descriptivas, tablas y visualizaciones.

## Dataset

El archivo utilizado es `netflix_titles.csv`, que contiene información sobre películas y series disponibles en Netflix.

Variables principales:

- `type`: tipo de contenido, película o serie.
- `title`: título.
- `director`: director.
- `cast`: elenco.
- `country`: país o países de producción.
- `date_added`: fecha en que el contenido fue agregado a Netflix.
- `release_year`: año de estreno.
- `rating`: clasificación del contenido.
- `duration`: duración en minutos o temporadas.
- `listed_in`: géneros o categorías.
- `description`: descripción del título.

## Funcionalidades

- Carga de archivo CSV.
- Limpieza de datos.
- Tratamiento de valores faltantes.
- Conversión de fechas y años.
- Creación de columnas nuevas.
- Métricas descriptivas.
- Filtros por tipo, año, país, clasificación y género.
- Tabla interactiva.
- Gráficos de barras y línea.

## Estructura del proyecto

```text
proyecto_progra/
├── README.md
├── requirements.txt
├── data/
│   └── netflix_titles.csv
├── src/
│   ├── app.py
│   ├── processing.py
│   └── viz.py
└── docs/
