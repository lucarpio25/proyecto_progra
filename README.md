# Dashboard del Catálogo de Netflix

## Descripción

Este proyecto corresponde a la entrega parcial del curso Programación Avanzada para la Ciencia de Datos.

La aplicación fue desarrollada en Streamlit y permite analizar un dataset del catálogo de Netflix mediante filtros interactivos, métricas descriptivas, tablas y visualizaciones.

## Dataset

El archivo utilizado es `netflix_titles.csv`, que contiene información sobre 8,807 películas y series disponibles en Netflix hasta mediados de 2021.
Fuente: Bansal, S. (2021). Netflix Movies and TV Shows [Dataset]. Kaggle.
https://www.kaggle.com/datasets/shivamb/netflix-shows
Licencia: CC0 1.0 Universal (dominio público).

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

## Procesamiento

La limpieza y transformación de datos se realizó en src/processing.py e incluyó:

- Eliminación de registros duplicados.
- Tratamiento de valores faltantes en columnas categóricas.
- Conversión de date_added a formato fecha y release_year a entero.
- Separación de la columna duration en valor numérico y unidad.
- Creación de columnas nuevas: year_added, month_added, main_country, main_genre y content_age.
- Métricas descriptivas: total de títulos, total de películas, total de series, países distintos y géneros distintos.

## Funcionalidades

- Carga de archivo CSV con manejo de errores.
- Limpieza y transformación de datos.
- Filtros interactivos por tipo de contenido, clasificación, país y rango de años.
- Métricas descriptivas en tarjetas.
- Tabla interactiva con datos filtrados.
- Gráficos: cantidad por tipo, distribución de clasificaciones, top géneros, top países y títulos por año.
- Top 10 títulos más recientes.

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
```

## Instalación y ejecución local

- Clona el repositorio:

`bashgit clone https://github.com/lucarpio25/proyecto_progra.git`

`cd proyecto_progra`

- Crea y activa un entorno virtual:

`bashpython3 -m venv mivenv`

`source mivenv/bin/activate`

- Instala las dependencias:

`bashpip install -r requirements.txt`

- Ejecuta la aplicación:

`bashstreamlit run src/app.py`

- Abre el navegador en http://localhost:8501.

## Referencias

- Rahmad, A. (2023). Netflix Data Analysis with Streamlit [Repositorio GitHub]. https://github.com/ahmadrahmadx/Netflix-Data-Analysis

Sirvió como referencia para la estructura del dashboard y la forma de presentar filtros por tipo de contenido y año.

- Streamlit. (2024). Streamlit Documentation. https://docs.streamlit.io

Documentación oficial utilizada para implementar los controles interactivos, métricas y visualizaciones de la app.
